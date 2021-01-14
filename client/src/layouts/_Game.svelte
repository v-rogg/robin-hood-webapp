<script lang="ts">
    import {PLAYERS_STORE} from "../stores";
    import {io} from "socket.io-client";
    import {onMount} from "svelte";
    import Dartboard from "../components/_Game/Dartboard.svelte";
    import Player from "../components/_Game/Player.svelte";
    import Stats from "../components/_Game/Stats.svelte";
    import Darts from "../components/_Game/Darts.svelte";

    const socket = io('ws://192.168.178.48:3000');

    const DART_TARGETS = INITIAL_DART_TARGETS;
    const DART_CHECKOUT = INITIAL_DART_CHECKOUT;

    onMount(() => {
        [d0, d1, d2] = INITIAL_DARTS;
        lastReceivedDarts = [d0, d1, d2];
        ready = true;
    })

    let [d0, d1, d2] = [0, 0, 0];
    let ready = false;
    let lastReceivedDarts = [0, 0, 0];

    function getPoints(d0, d1, d2) {
        const selectNodes = document.getElementsByTagName('select');
        for (let node of selectNodes) {
            node.classList.remove('highlight--error');
        }
        if ((d0 != lastReceivedDarts[0] || d1 != lastReceivedDarts[1] || d2 != lastReceivedDarts[2]) && ready) {
            socket.emit('setDarts', JSON.stringify([d0, d1, d2]))
        }
        return DART_TARGETS[d0].value + DART_TARGETS[d1].value + DART_TARGETS[d2].value
    }

    $: points = getPoints(d0, d1, d2);

    socket.on('darts', data => {
        lastReceivedDarts = [d0, d1, d2];
        [d0, d1, d2] = JSON.parse(data);
        ready = false
        setTimeout(() => {
            ready = true
        }, 500)
    })

    let players;
    PLAYERS_STORE.subscribe(value => players = value);

    function getCurrentPlayer(players) {
        let currentPlayer = {
            name: null,
            uuid: null,
            points: null,
            active: null,
            id: 0
        };
        for (let i = 0; i < players.length; i++) {
            if (players[i].active) {
                currentPlayer = players[i]
                currentPlayer.id = i
            }
        }
        return currentPlayer;
    }

    $: currentPlayer = getCurrentPlayer(players);


    function getSuggestion(points, [d0, d1, d2]) {
        let throwsLeft = 3;
        [d0, d1, d2].forEach(d => {
            if (DART_TARGETS[d].name !== "") throwsLeft--;
        })
        const pointsLeft = currentPlayer.points - points;
        const DC = DART_CHECKOUT.find(e => e.left === pointsLeft && e.darts.length <= throwsLeft);
        console.log(DC);
        if (DC) {
            const simpleSug = [...DC.darts];
            let complexSug = [];
            [d0, d1, d2].forEach(d => {
                if (DART_TARGETS[d].name !== "") {
                    complexSug.push(null)
                } else {
                    complexSug.push(simpleSug.shift())
                }
            })
            return complexSug;
        } else {
            return [];
        }
    }

    $: suggestion = getSuggestion(points, [d0, d1, d2]);

</script>

<Dartboard/>
<Darts bind:d0={d0} bind:d1={d1} bind:d2={d2} {currentPlayer} {DART_TARGETS} {suggestion}/>
<Player/>
<Stats {currentPlayer} {points} {d0} {d1} {d2} {players} {DART_TARGETS}/>

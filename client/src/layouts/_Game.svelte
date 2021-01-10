<script lang="ts">
    import {PLAYERS_STORE} from "../stores";
    import {io} from "socket.io-client";
    import {onMount} from "svelte";
    import Dartboard from "../components/_Game/Dartboard.svelte";
    import Player from "../components/_Game/Player.svelte";
    import Stats from "../components/_Game/Stats.svelte";
    import Darts from "../components/_Game/Darts.svelte";

    const socket = io('ws://192.168.178.48:3000');

    let DART_TARGETS = INITIAL_DART_TARGETS;

    onMount(() => {
        [d0, d1, d2] = INITIAL_DARTS;
        lastReceivedDarts = [d0, d1, d2];
        ready = true;
    })

    let [d0, d1, d2] = [0, 0, 0];
    let ready = false;
    let lastReceivedDarts = [0, 0, 0];

    function getPoints(d0, d1, d2) {
        if ((d0 != lastReceivedDarts[0] || d1 != lastReceivedDarts[1] || d2 != lastReceivedDarts[2]) && ready) {
            socket.emit('setDarts', JSON.stringify([d0, d1, d2]))
        }
        return DART_TARGETS[d0].value + DART_TARGETS[d1].value + DART_TARGETS[d2].value
    }

    $: points = getPoints(d0, d1, d2)

    socket.on('darts', data => {
        lastReceivedDarts = [d0, d1, d2];
        [d0, d1, d2] = JSON.parse(data);
        ready = false
        setTimeout(() => {
            ready = true
        }, 500)
    })

    let players;
    PLAYERS_STORE.subscribe(value => players = value)

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

    $: currentPlayer = getCurrentPlayer(players)

</script>

<Dartboard/>
<Darts bind:d0={d0} bind:d1={d1} bind:d2={d2} {DART_TARGETS} />
<Player/>
<Stats {currentPlayer} {points} {d0} {d1} {d2} {players} {DART_TARGETS} />

<script lang="ts">
    import {PLAYERS_STORE} from "../stores";
    import {io} from "socket.io-client";
    import {onMount} from "svelte";
    import Dartboard from "../components/_Game/Dartboard.svelte";
    import Player from "../components/_Game/Player.svelte";
    import Stats from "../components/_Game/Stats.svelte";
    import Darts from "../components/_Game/Darts.svelte";

    const socket = io(ws_socket);

    const DART_TARGETS = INITIAL_DART_TARGETS;
    const DART_CHECKOUT = INITIAL_DART_CHECKOUT;

    let [d0, d1, d2] = [0, 0, 0];
    let lastReceivedDarts = [0, 0, 0];
    let sensor_darts = INITIAL_LAST_SENSOR_DARTS;
    let ready = false;
    let darts = [0, 0, 0];

    onMount(() => {
        [d0, d1, d2] = INITIAL_DARTS;
        lastReceivedDarts = [d0, d1, d2];
        ready = true;
    })


    function getPoints(d0, d1, d2, darts) {
        const selectNodes = document.getElementsByTagName('select');
        for (let node of selectNodes) {
            node.classList.remove('highlight--error');
        }
        // if (d0 == darts[0] && d1 == darts[1] && d2 == darts[2]) {
            if ((d0 != lastReceivedDarts[0] || d1 != lastReceivedDarts[1] || d2 != lastReceivedDarts[2]) && ready) {
                socket.emit('setDarts', JSON.stringify([d0, d1, d2]))
            }
        // }

        return DART_TARGETS[darts[0]].value + DART_TARGETS[darts[1]].value + DART_TARGETS[darts[2]].value
    }

    $: points = getPoints(d0, d1, d2, darts);

    socket.on('darts', data => {
        lastReceivedDarts = [d0, d1, d2];
        [d0, d1, d2] = JSON.parse(data);
        ready = false
        setTimeout(() => {
            ready = true
        }, 250)
    })

    socket.on('sensorDarts', data => {
        sensor_darts = JSON.parse(data);
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

    function getSuggestion(points, darts, players) {
        let throwsLeft = 3;
        darts.forEach(d => {
            if (DART_TARGETS[d].name !== "") throwsLeft--;
        })
        const pointsLeft = currentPlayer.points - points;
        const DC = DART_CHECKOUT.find(e => e.left === pointsLeft && e.darts.length <= throwsLeft);
        if (DC) {
            const simpleSug = [...DC.darts];
            let complexSug = [];
            darts.forEach(d => {
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

    $: suggestion = getSuggestion(points, darts, players);

    function combineDarts(sensor_darts, form_darts) {
        let array = [0, 0, 0]
        for (let i = 0; i < 3; i++) {
            if (DART_TARGETS[form_darts[i]].type !== 'none') {
                array[i] = form_darts[i]
            } else if (sensor_darts[i] != null) {
                array[i] = sensor_darts[i][2]
            } else
                array[i] = 0
        }
        return array
    }

    $: darts = combineDarts(sensor_darts, [d0, d1, d2]);

</script>

<Dartboard {sensor_darts} {players}/>
<Darts bind:d0={d0} bind:d1={d1} bind:d2={d2} {sensor_darts} {currentPlayer} {DART_TARGETS} {suggestion}/>
<!--<Darts bind:d0={d0} bind:d1={d1} bind:d2={d2} {sensor_darts} {currentPlayer} {DART_TARGETS}/>-->
<Player/>
<Stats {currentPlayer} {points} {players} {DART_TARGETS} {darts}/>

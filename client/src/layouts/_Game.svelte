<script lang="ts">
    import {DARTS_STORE, PLAYERS_STORE} from "../stores";
    import {io} from "socket.io-client";
    import {onMount} from "svelte";

    const socket = io('ws://192.168.178.48:3000');

    let DART_TARGETS = INITIAL_DART_TARGETS;

    onMount(() => {
        [d0, d1, d2] = $DARTS_STORE;
        lastReceivedDarts = $DARTS_STORE;
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

    function getCurrentPlayer(x) {
        let currentPlayer = {
            name: null,
            uuid: null,
            points: null,
            active: null,
            id: 0
        };
        for(let i = 0; i<players.length; i++) {
            if (players[i].active) {
                currentPlayer = players[i]
                currentPlayer.id = i
            }
        }
        return currentPlayer;
    }

    $: currentPlayer = getCurrentPlayer(players)
</script>

<style lang="sass">
    @import "src/styles/theme"

    #dartboard
        max-height: 300px
        max-width: 300px

    form
        margin-top: 20px
        display: flex
        justify-content: center
        gap: 1rem

        select
            font-size: 4rem
            font-weight: 300
            width: 150px
            border: none
            border-bottom: 1px solid black
            outline: none
            text-align: center
            -webkit-appearance: none
            -moz-appearance: none
            text-indent: 1px
            text-overflow: ''

            option
                font-size: 1rem
                color: black

        .label
            height: 2rem
            margin-top: .5rem
            font-size: 1.125rem

    #stats
        display: flex
        justify-content: space-between
        border-bottom: 1px solid $grey

    #player
        background: $black
        color: white
        margin-top: 20px
        font-size: 1.5rem
        height: 60px
        display: flex
        justify-content: center
        align-items: center

        .even
            border-color: $red !important
            color: $red !important

        span
            border: 2px solid $green
            color: $green
            font-weight: 700
            font-size: 0.825rem
            border-radius: 100%
            width: 18px
            height: 18px
            position: relative
            display: flex
            align-items: center
            justify-content: center
            pointer-events: none
            //margin-bottom: .25rem
            line-height: 0
            margin-right: .5rem

    #scores
        background: $lightgrey
        border-right: 1px solid $grey
        width: clamp(100px, 15vw, 200px)
        padding-top: 1rem

    #points
        background: none
        border: none
        width: 100%
        height: 100%
        display: flex
        justify-content: center
        align-items: center
        user-select: none

        &:hover
            cursor: pointer

        &:active
            border-style: none
            background: $lightgrey

        #points

            &__box
                //margin: 40px 0 calc(40px + 1.5rem)
                //width: 10rem
                width: max-content
                display: flex
                flex-direction: column
                align-self: center
                height: 100%

            &__turn
                color: $green
                font-size: 1.5rem
                align-self: flex-end
                height: 1.5rem
                margin-top: 1.8rem

            &__total
                font-size: 6rem
                font-weight: 500
                line-height: 0.9
                margin-bottom: 1.5rem

            &__description
                font-size: 0.9rem
                color: $grey
                margin-bottom: 0.9rem

    #opponents
        border-left: 1px solid $grey
        width: clamp(100px, 15vw, 200px)
        padding-top: 1rem

    .beige
        color: $beige
    .green
        color: $green
    .red
        color: $red
    .grey
        color: $grey

</style>

<picture>
    <source src="/app/dartboard-small.webp" type="image/webp">
    <img id="dartboard" src="/app/dartboard-small.png" type="image/png" alt="Dartboard">
</picture>

<form id="darts">
    <div>
        <select form="darts" bind:value={d0} class={DART_TARGETS[d0].color}>
            {#each DART_TARGETS as {name, color}, id}
                <option value={id}>{name}</option>
            {/each}
        </select>
        <div class="label">
            {#if DART_TARGETS[d0].type !== 'single'}
                <span>{DART_TARGETS[d0].value}</span>
            {/if}
        </div>
    </div>
    <div>
        <select form="darts" bind:value={d1} class={DART_TARGETS[d1].color}>
            {#each DART_TARGETS as {name}, id}
                <option value={id}>{name}</option>
            {/each}
        </select>
        <div class="label">
            {#if DART_TARGETS[d1].type !== 'single'}
                <span>{DART_TARGETS[d1].value}</span>
            {/if}
        </div>
    </div>
    <div>
        <select form="darts" bind:value={d2} class={DART_TARGETS[d2].color}>
            {#each DART_TARGETS as {name}, id}
                <option value={id}>{name}</option>
            {/each}
        </select>
        <div class="label">
            {#if DART_TARGETS[d2].type !== 'single'}
                <span>{DART_TARGETS[d2].value}</span>
            {/if}
        </div>
    </div>
    <button type="submit" hidden></button>
</form>

<div id="player">
    <span class:even={(currentPlayer.id + 1) % 2 === 0}>{ currentPlayer.id + 1 }</span>
    { currentPlayer.name }
</div>

<div id="stats">
    <div id="scores">
        Scores
    </div>
    <button id="points" on:click={() => { fetch('/api/next-player', {method: 'POST'}) }}>
        <div id="points__box">
            <div id="points__turn">
                {#if points > 0}
                    { -points }
                {/if}
            </div>
            <div id="points__total">
                { currentPlayer.points - points }
            </div>
            <div id="points__description">
                Click to Confirm
            </div>
        </div>
    </button>
    <div id="opponents">
        {#each players as {name, points, active}}
            {#if !active}
                <div>
                    {name}
                    <br/>
                    <span class="grey">
                        {points}
                    </span>
                </div>
                <br/>
            {/if}
        {/each}
    </div>
</div>

<!--<button on:click={() => { fetch('/api/next-player', {method: 'POST'}) }}>Next Player</button>-->
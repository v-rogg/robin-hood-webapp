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

    function getCurrentPlayer(players) {
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

    function getPointsColor(currentPlayer, points, d0, d1, d2, DART_TARGETS): string {
        let win = false
        if (currentPlayer.points - points === 0) {
            let check = [d0, d1, d2]
            for (let i = 2; i >= 0; i--) {
                if (DART_TARGETS[check[i]].type == 'double') {
                    win = true
                }
            }
        }
        if (win) {
            return 'green';
        } else if (currentPlayer.points - points <= 0) {
            return 'red';
        }
        else {
            return 'black';
        }

    }

    $: pointsColor = getPointsColor(currentPlayer, points, d0, d1, d2, DART_TARGETS)
</script>

<style lang="sass">
    @import "src/styles/theme"

    #dartboard
        display: flex
        flex-direction: column

        #live
            align-self: flex-end
            margin-right: 3rem
            margin-bottom: -14px

        img
            max-height: 300px
            max-width: 300px


    form
        margin-top: 40px
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
            line-height: 0
            margin-right: .5rem

    #scores
        background: $lightgrey
        border-right: 1px solid $grey
        width: clamp(100px, 15vw, 200px)
        padding: 1rem 0

        ul
            list-style: none
            padding: 0
            margin: 0.5rem 0 0

            li
                color: $darkgrey

    #points
        background: none
        border: none
        flex-grow: 1
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
                width: max-content
                display: flex
                flex-direction: column
                align-self: center

            &__box-small
                height: 1.5rem
                margin-top: 1.8rem
                display: flex
                justify-content: space-between

            &__total
                font-size: 1.5rem
                color: $grey

            &__turn
                color: $green
                font-size: 1.5rem

            &__total-minus
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
        padding: 1rem 0

    .beige
        color: $beige
    .green
        color: $green
    .red
        color: $red
    .grey
        color: $grey

</style>

<div id="dartboard">
<!--    <svg id="live" width="40" height="17.5" viewBox="0 0 32 14" fill="none" xmlns="http://www.w3.org/2000/svg">-->
<!--        <rect width="32" height="14" rx="5" fill="#E8472F"/>-->
<!--        <path d="M13.48 10.25C13.4133 10.25 13.3567 10.23 13.31 10.19C13.27 10.1433 13.25 10.0867 13.25 10.02V3.38C13.25 3.31333 13.27 3.26 13.31 3.22C13.3567 3.17333 13.4133 3.15 13.48 3.15H13.95C14.0167 3.15 14.07 3.17333 14.11 3.22C14.1567 3.26 14.18 3.31333 14.18 3.38V10.02C14.18 10.0867 14.1567 10.1433 14.11 10.19C14.07 10.23 14.0167 10.25 13.95 10.25H13.48ZM15.8216 4.08C15.755 4.08 15.6983 4.06 15.6516 4.02C15.6116 3.97333 15.5916 3.91667 15.5916 3.85V3.31C15.5916 3.24333 15.6116 3.18667 15.6516 3.14C15.6983 3.09333 15.755 3.07 15.8216 3.07H16.4516C16.5183 3.07 16.575 3.09333 16.6216 3.14C16.6683 3.18667 16.6916 3.24333 16.6916 3.31V3.85C16.6916 3.91667 16.6683 3.97333 16.6216 4.02C16.575 4.06 16.5183 4.08 16.4516 4.08H15.8216ZM15.9016 10.25C15.835 10.25 15.7783 10.23 15.7316 10.19C15.6916 10.1433 15.6716 10.0867 15.6716 10.02V5.28C15.6716 5.21333 15.6916 5.16 15.7316 5.12C15.7783 5.07333 15.835 5.05 15.9016 5.05H16.3816C16.4483 5.05 16.5016 5.07333 16.5416 5.12C16.5883 5.16 16.6116 5.21333 16.6116 5.28V10.02C16.6116 10.0867 16.5883 10.1433 16.5416 10.19C16.5016 10.23 16.4483 10.25 16.3816 10.25H15.9016ZM19.9035 10.25C19.7302 10.25 19.6068 10.1667 19.5335 10L17.6835 5.36L17.6635 5.26C17.6635 5.2 17.6835 5.15 17.7235 5.11C17.7635 5.07 17.8135 5.05 17.8735 5.05H18.3535C18.4668 5.05 18.5502 5.10667 18.6035 5.22L20.1235 9.16L21.6435 5.22C21.7035 5.10667 21.7835 5.05 21.8835 5.05H22.3735C22.4268 5.05 22.4735 5.07 22.5135 5.11C22.5602 5.15 22.5835 5.2 22.5835 5.26L22.5635 5.36L20.7035 10C20.6302 10.1667 20.5068 10.25 20.3335 10.25H19.9035ZM25.5251 10.35C24.8384 10.35 24.2884 10.14 23.8751 9.72C23.4684 9.29333 23.2451 8.71333 23.2051 7.98L23.1951 7.64L23.2051 7.31C23.2517 6.59 23.4784 6.01667 23.8851 5.59C24.2984 5.16333 24.8417 4.95 25.5151 4.95C26.2551 4.95 26.8284 5.18667 27.2351 5.66C27.6417 6.12667 27.8451 6.76 27.8451 7.56V7.73C27.8451 7.79667 27.8217 7.85333 27.7751 7.9C27.7351 7.94 27.6817 7.96 27.6151 7.96H24.1551V8.05C24.1751 8.48333 24.3051 8.85333 24.5451 9.16C24.7917 9.46 25.1151 9.61 25.5151 9.61C25.8217 9.61 26.0717 9.55 26.2651 9.43C26.4651 9.30333 26.6117 9.17333 26.7051 9.04C26.7651 8.96 26.8084 8.91333 26.8351 8.9C26.8684 8.88 26.9251 8.87 27.0051 8.87H27.4951C27.5551 8.87 27.6051 8.88667 27.6451 8.92C27.6851 8.95333 27.7051 9 27.7051 9.06C27.7051 9.20667 27.6117 9.38333 27.4251 9.59C27.2451 9.79667 26.9884 9.97667 26.6551 10.13C26.3284 10.2767 25.9517 10.35 25.5251 10.35ZM26.8951 7.27V7.24C26.8951 6.78 26.7684 6.40667 26.5151 6.12C26.2684 5.82667 25.9351 5.68 25.5151 5.68C25.0951 5.68 24.7617 5.82667 24.5151 6.12C24.2751 6.40667 24.1551 6.78 24.1551 7.24V7.27H26.8951Z" fill="white"/>-->
<!--        <circle cx="7" cy="7" r="3" fill="white"/>-->
<!--    </svg>-->

    <picture>
        <source src="/app/dartboard-small.webp" type="image/webp">
        <img src="/app/dartboard-small.png" type="image/png" alt="Dartboard">
    </picture>
</div>


<form id="darts">
    <div>
        <select form="darts" bind:value={d0} class={DART_TARGETS[d0].color}>
            {#each DART_TARGETS as {name}, id}
                <option value={id}>{name}</option>
            {/each}
        </select>
        <div class="label">
            {#if DART_TARGETS[d0].type !== 'single' && DART_TARGETS[d0].type !== 'none'}
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
            {#if DART_TARGETS[d1].type !== 'single' && DART_TARGETS[d1].type !== 'none'}
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
            {#if DART_TARGETS[d2].type !== 'single' && DART_TARGETS[d2].type !== 'none'}
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
        <ul class="darkgrey">
            {#if currentPlayer.turns }
                {#each currentPlayer.turns as turn}
                    <li>{ DART_TARGETS[turn[0]].value + DART_TARGETS[turn[1]].value + DART_TARGETS[turn[2]].value }</li>
                {/each}
            {/if}
        </ul>
    </div>
    <button id="points" on:click={() => { fetch('/api/confirm-turn', {method: 'POST'}) }}>
        <div id="points__box">
            <div id="points__box-small">
                <div id="points__total">
                    {#if points > 0 }
                        { currentPlayer.points }
                    {/if}
                </div>
                <div id="points__turn">
                    {#if points > 0}
                        { -points }
                    {/if}
                </div>
            </div>
            <div id="points__total-minus" class:red={pointsColor === 'red'} class:green={pointsColor === 'green'}>
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
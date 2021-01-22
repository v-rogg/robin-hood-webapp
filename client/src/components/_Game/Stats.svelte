<script lang="ts">
    export let DART_TARGETS;
    export let currentPlayer;
    export let points;
    export let players;
    // export let d0;
    // export let d1;
    // export let d2;
    export let darts;

    function getPointsColor(currentPlayer, points, darts) {
        let win = false
        if (currentPlayer.points - points === 0) {
            let check = darts
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
        } else {
            return 'black';
        }

    }

    $: pointsColor = getPointsColor(currentPlayer, points, darts)

    function getConfirmEnabled(darts) {
        if (currentPlayer.points - points > 0) {
            return !(DART_TARGETS[darts[0]].name === "" || DART_TARGETS[darts[1]].name === "" || DART_TARGETS[darts[2]].name === "");
        } else {
            return true
        }
    }

    $: confirmEnabled = getConfirmEnabled(darts)

    function highlightForms() {
        const selectNodes = document.getElementsByTagName('select');
        console.log(selectNodes);
        for (let node of selectNodes) {
            if (node.id === "d0") {
                if (DART_TARGETS[darts[0]].name === "") {
                    node.classList.add('highlight--error');
                }
            } else if (node.id === "d1") {
                if (DART_TARGETS[darts[1]].name === "") {
                    node.classList.add('highlight--error');
                }
            } else if (node.id === "d2") {
                if (DART_TARGETS[darts[2]].name === "") {
                    node.classList.add('highlight--error');
                }
            }
        }
    }
</script>

<style lang="sass">
    @import "src/styles/theme"

    #stats
        display: flex
        justify-content: space-between
        border-bottom: 1px solid $grey

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
    <button id="points" on:click={() => { confirmEnabled ? fetch('/api/confirm-turn', {method: 'POST'}) : highlightForms() }}>
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
                {#if confirmEnabled}
                    Click to Confirm
                {:else}
                    <br/>
                {/if}
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
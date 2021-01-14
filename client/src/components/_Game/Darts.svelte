<script lang="ts">
    export let DART_TARGETS;
    export let currentPlayer;
    export let d0;
    export let d1;
    export let d2;
    export let suggestion;
</script>

<style lang="sass">
    @import "src/styles/theme"

    form
        margin-top: 40px
        display: flex
        justify-content: center
        gap: 1rem

        >div
            position: relative

        select
            font-size: 4rem
            font-weight: 300
            width: 150px
            //border: 1px solid transparent
            border: none
            border-bottom: 1px solid black
            outline: none
            text-align: center
            -webkit-appearance: none
            -moz-appearance: none
            text-indent: 1px
            text-overflow: ''
            cursor: pointer
            background: transparent
            transition: border ease 100ms, background ease 100ms

            option
                font-size: 1rem
                color: black
                background: white

        .label
            height: 2rem
            margin-top: .5rem
            font-size: 1.125rem

        .suggestion
            position: absolute
            font-size: 1.5rem
            //color: $blue
            color: $orange
            top: .25rem
            right: .5rem
            pointer-events: none

    .beige
        color: darken($beige, 15)
    .green
        color: $green
    .red
        color: $red
    .grey
        color: $grey

    .highlight--error
        border-bottom: 1px solid $red
        background: transparentize($red, .95)

    @media (max-width: 520px)
        form
            select
                font-size: 3.25rem
                width: clamp(100px, 25vw, 150px)

    @media (max-width: 420px)
        form
            select
                font-size: 2.825rem

</style>

<form id="darts">
    <div>
        <select id="d0" form="darts" bind:value={d0} class={DART_TARGETS[d0].color}>
            {#each DART_TARGETS as {name}, id}
                <option value={id}>{name}</option>
            {/each}
        </select>
        <div class="label">
            {#if DART_TARGETS[d0].type !== 'single' && DART_TARGETS[d0].type !== 'none'}
                <span>{DART_TARGETS[d0].value}</span>
            {/if}
        </div>
        {#if suggestion[0] && currentPlayer.checkout}
            <div class="suggestion">
                {suggestion[0]}
            </div>
        {/if}
    </div>
    <div>
        <select id="d1" form="darts" bind:value={d1} class={DART_TARGETS[d1].color}>
            {#each DART_TARGETS as {name}, id}
                <option value={id}>{name}</option>
            {/each}
        </select>
        <div class="label">
            {#if DART_TARGETS[d1].type !== 'single' && DART_TARGETS[d1].type !== 'none'}
                <span>{DART_TARGETS[d1].value}</span>
            {/if}
        </div>
        {#if suggestion[1] && currentPlayer.checkout}
            <div class="suggestion">
                {suggestion[1]}
            </div>
        {/if}
    </div>
    <div>
        <select id="d2" form="darts" bind:value={d2} class={DART_TARGETS[d2].color}>
            {#each DART_TARGETS as {name}, id}
                <option value={id}>{name}</option>
            {/each}
        </select>
        <div class="label">
            {#if DART_TARGETS[d2].type !== 'single' && DART_TARGETS[d2].type !== 'none'}
                <span>{DART_TARGETS[d2].value}</span>
            {/if}
        </div>
        {#if suggestion[2] && currentPlayer.checkout}
            <div class="suggestion">
                {suggestion[2]}
            </div>
        {/if}
    </div>
    <button type="submit" hidden></button>
</form>
<script lang="ts">
    export let DART_TARGETS;
    export let currentPlayer;
    export let d0;
    export let d1;
    export let d2;
    export let suggestion;
    export let sensor_darts;

    function get_sensor_darts_targets(sensor_darts) {
        let array = [];
        for(let i = 0; i < sensor_darts.length; i++) {
            if(sensor_darts[i][2] !== undefined) {
                array.push(DART_TARGETS[sensor_darts[i][2]].name)
            }
        }
        return array;
    }

    $: sensor_darts_targets = get_sensor_darts_targets(sensor_darts);

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
            z-index: 2
            position: absolute
            font-size: 1.5rem
            color: $orange
            top: .25rem
            right: .5rem
            pointer-events: none

        .sensor_dart_target
            &--small, &--big
                position: absolute
                color: $blue

            &--small
                top: .25rem
                left: .5rem
                font-size: 1.5rem
                pointer-events: none

            &--big
                font-size: 4rem
                font-weight: 300
                width: 150px
                top: 0
                left: 0
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

            .sensor_dart_target--big
                width: clamp(100px, 25vw, 150px) !important

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
            {#if DART_TARGETS[d0].type === 'double' || DART_TARGETS[d0].type === 'triple'}
                <span>{DART_TARGETS[d0].value}</span>
            {/if}
        </div>
        {#if suggestion[0] && currentPlayer.checkout}
            <div class="suggestion">
                {suggestion[0]}
            </div>
        {/if}
        {#if sensor_darts_targets[0]}
            <div class:sensor_dart_target--big={DART_TARGETS[d0].type === 'none'}
                 class:sensor_dart_target--small={DART_TARGETS[d0].type !== 'none'}>
                {sensor_darts_targets[0]}
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
            {#if DART_TARGETS[d1].type === 'double' || DART_TARGETS[d1].type === 'triple'}
                <span>{DART_TARGETS[d1].value}</span>
            {/if}
        </div>
        {#if suggestion[1] && currentPlayer.checkout}
            <div class="suggestion">
                {suggestion[1]}
            </div>
        {/if}
        {#if sensor_darts_targets[1]}
            <div class:sensor_dart_target--big={DART_TARGETS[d1].type === 'none'}
                 class:sensor_dart_target--small={DART_TARGETS[d1].type !== 'none'}>
                {sensor_darts_targets[1]}
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
            {#if DART_TARGETS[d2].type === 'double' || DART_TARGETS[d2].type === 'triple'}
                <span>{DART_TARGETS[d2].value}</span>
            {/if}
        </div>
        {#if suggestion[2] && currentPlayer.checkout}
            <div class="suggestion">
                {suggestion[2]}
            </div>
        {/if}
        {#if sensor_darts_targets[2]}
            <div class:sensor_dart_target--big={DART_TARGETS[d2].type === 'none'}
                 class:sensor_dart_target--small={DART_TARGETS[d2].type !== 'none'}>
                {sensor_darts_targets[2]}
            </div>
        {/if}
    </div>
    <button type="submit" hidden></button>
</form>

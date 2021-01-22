<script lang="ts">
    import Two from "./Two.svelte";

    export let sensor_darts;
    export let players;
</script>

<style lang="sass">
    #dartboard
        display: flex
        flex-direction: column
        position: relative

        #live
            align-self: flex-end
            margin-right: 3rem
            margin-bottom: -14px

        img
            max-height: 300px
            max-width: 300px

    #two
        position: absolute
        width: 300px
        margin: 0 auto
        left: 0
        right: 0
</style>

<div id="dartboard">
    <picture>
        <source src="/app/unicorn-small.webp" type="image/webp">
        <img src="/app/unicorn-small.png" type="image/png" alt="Dartboard">
    </picture>
    <Two {sensor_darts} {players}/>
</div>
<script lang="ts">
    import PlayerList from "../components/_NewGame/PlayerList.svelte";
    import GameMode from "../components/_NewGame/GameMode.svelte";
    import StartButton from "../components/_NewGame/StartButton.svelte";
    import Legend from "../components/_NewGame/Legend.svelte";
</script>

<style lang="sass">
    h1, h2
        margin: 0
        padding: 0

    h1
        font-size: 3rem
        font-weight: 600

    h2
        font-size: 1.5rem
        font-weight: 300


    #bottom
        display: flex
        justify-content: space-between
</style>

<h1>New Game</h1>
<h2>Players & Game Mode</h2>
<PlayerList/>
<GameMode/>

<div id="bottom">
    <Legend/>
    <StartButton/>
</div>

<script lang="ts">
    import PlayerList from "../components/_NewGame/PlayerList.svelte";
    import GameMode from "../components/_NewGame/GameMode.svelte";
    import StartButton from "../components/_NewGame/StartButton.svelte";

    // function switchMode() {
    //     switch (CLIENT_STATE) {
    //         case 'New Game':
    //             CLIENT_STATE_STORE.set('Add Players');
    //             break;
    //         case 'Add Players':
    //             CLIENT_STATE_STORE.set('New Game');
    //             break;
    //     }
    // }
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
</style>

<h1>New Game</h1>
<h2>Players & Game Mode</h2>

<PlayerList/>
<GameMode/>
<StartButton/>
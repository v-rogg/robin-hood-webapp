<script lang="ts">
    import {players_store} from "../../stores";

    let players;

    players_store.subscribe(value => players= value);
</script>

<style lang="sass">
    ul
        width: 10em
        margin: 1rem auto 0
        text-align: left
</style>

<h1>Game is running</h1>
<ul>
    {#each players as {first_name, last_name}}
        <li>
            {first_name} {last_name}
        </li>
    {/each}
</ul>
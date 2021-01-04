<script lang="ts">
    import {players} from "../../stores";

    let players_value;

    players.subscribe(value => players_value = value);
</script>

<style lang="sass">
    ul
        width: 10em
        margin: 1rem auto 0
        text-align: left
</style>

<h1>Game is running</h1>
<ul>
    {#each players_value as {first_name, last_name}}
        <li>
            {first_name} {last_name}
        </li>
    {/each}
</ul>
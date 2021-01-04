<script lang="ts">
    import {onMount} from 'svelte';

    let rand = -1;

    function getRand() {
        fetch("/api/rand")
            .then(res => res.text())
            .then(d => (rand = parseInt(d)));
    }

    onMount(async () => {
        getRand();
    })
</script>

<style lang="sass">
    h1
        font-size: 2em
        font-weight: 400
</style>

<h1>Your number is <strong>{rand}</strong>!</h1>
<button on:click={getRand}>Get a random number</button>


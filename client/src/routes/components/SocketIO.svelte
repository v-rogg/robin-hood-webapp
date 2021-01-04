<script lang="ts">
    import {io} from 'socket.io-client';

    const socket = io('ws://localhost:3000');

    let text;
    let message = [];

    socket.on('connect', () => {
        socket.emit('message', `Connected ${navigator.userAgent}`);
    });

    socket.on('response', (msg) => {
        console.log(`server: ${msg}`);
        message = [...message, msg];
    });

    function send() {
        socket.emit('message', text);
        console.log(`client: ${text}`);
    }
</script>

<style lang="sass">
    ul
        text-align: left
        list-style: none
</style>

<form on:submit|preventDefault={send}>
    <input type="text" placeholder="Messages" bind:value={text}/>
    <button type="submit">Send</button>
</form>

<ul>
    {#each message as msg}
        <li>
            {msg}
        </li>
    {/each}
</ul>

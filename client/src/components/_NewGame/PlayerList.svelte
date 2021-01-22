<script lang="ts">
    import {io} from "socket.io-client";
    import {PLAYERS_STORE} from "../../stores";
    const socket = io(ws_socket);

    let name;
    let players;
    PLAYERS_STORE.subscribe(value => players = value);

    function removePlayer(id) {
        socket.emit('removePlayer', JSON.stringify(players.find(({uuid}) => uuid === id)))
    }

    function togglePlayerCheckout(id) {
        socket.emit('togglePlayerCheckout', JSON.stringify(players.find(({uuid}) => uuid === id)))
    }

    function addPlayer() {
        if (name != "") {
            let user = {
                name: name,
            }
            name = "";
            socket.emit('addPlayer', JSON.stringify(user));
        }
    }
</script>

<style lang="sass">
    @import "src/styles/theme"

    ul
        list-style: none
        padding: 0
        margin: 80px 0 0

    li
        height: 80px
        font-size: 1.5rem
        font-weight: 500
        display: flex
        padding: 0 3rem
        justify-content: space-between
        align-items: center
        border-top: 1px solid $grey

        >*
            display: flex
            flex-direction: column
            align-items: center
            justify-content: center

        &:nth-child(2n+1)
            background: $beige

        &:nth-child(2n+1)
            span
                color: $green
                border-color: $green

        &:nth-child(2n)
            span
                color: $red
                border-color: $red

        &:last-of-type
            border-bottom: 1px solid $grey

        //&:hover
            //cursor: pointer

        //    div
        //        color: $red
        //        text-decoration: line-through

        .name
            height: 1.75rem
            pointer-events: none

        span
            border: 2px solid $grey
            color: $grey
            font-weight: 700
            font-size: 0.825rem
            border-radius: 100%
            width: 18px
            height: 18px
            position: relative
            display: flex
            align-items: center
            justify-content: center
            pointer-events: none
            margin-bottom: .25rem
            line-height: 0

    .svg__bolt, .svg__remove
        width: 1.5rem
        height: 1.5rem

    .svg__bolt
        fill: transparent
        &--enabled
            fill: $orange
        &--disabled
            fill: $grey

    .bolt
        &:hover
            .svg__bolt
                &--enabled
                    fill: $grey
                &--disabled
                    fill: $orange

        &:active
            .svg__bolt
                &--enabled
                    fill: darken($grey, 15)
                &--disabled
                    fill: $red

    .remove
        &:hover
            fill: $orange
        &:active
            fill: $red

    .add
        font-weight: 300
        background: $black !important
        flex-direction: column
        justify-content: center

        &:hover
            background: lighten($black, 10) !important

        span
            color: white !important
            border-color: white !important

        form
            width: 100%
            height: 1.75rem

        input
            background: none
            border: none
            width: 95%
            text-align: center
            font-size: 1.5rem
            color: white
            outline-style: none

            &::placeholder
                color: white
                font-weight: 100

    button
        background: none
        border: none
        outline: none
        padding: 0
        margin: 0

        &:hover
            cursor: pointer
</style>

<ul id="playerlist">
    {#each players as {name, uuid, points, checkout}, nr}
        <li id="{uuid}">
            <button class="bolt" on:click={() => {togglePlayerCheckout(uuid)}}>
                <svg class="svg__bolt" class:svg__bolt--enabled={checkout} class:svg__bolt--disabled={!checkout} viewBox="0 0 192 192" xmlns="http://www.w3.org/2000/svg"><path d="m155.109 74.028a4 4 0 0 0 -3.48-2.028h-52.4l8.785-67.123a4.023 4.023 0 0 0 -7.373-2.614l-63.724 111.642a4 4 0 0 0 3.407 6.095h51.617l-6.962 67.224a4.024 4.024 0 0 0 7.411 2.461l62.671-111.63a4 4 0 0 0 .048-4.027z"/></svg>
            </button>
            <div class="mid">
                <span>{nr + 1}</span>
                <div class="name">
                    {name}
                </div>
            </div>
            <button on:click={() => {removePlayer(uuid)}} class="remove">
                <svg class="svg__remove" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg"><path d="m256 512c-141.164062 0-256-114.835938-256-256s114.835938-256 256-256 256 114.835938 256 256-114.835938 256-256 256zm0-480c-123.519531 0-224 100.480469-224 224s100.480469 224 224 224 224-100.480469 224-224-100.480469-224-224-224zm0 0"/><path d="m176.8125 351.1875c-4.097656 0-8.195312-1.554688-11.308594-4.691406-6.25-6.25-6.25-16.382813 0-22.632813l158.398438-158.402343c6.253906-6.25 16.386718-6.25 22.636718 0s6.25 16.382812 0 22.636718l-158.402343 158.398438c-3.15625 3.136718-7.25 4.691406-11.324219 4.691406zm0 0"/><path d="m335.1875 351.1875c-4.09375 0-8.191406-1.554688-11.304688-4.691406l-158.398437-158.378906c-6.253906-6.25-6.253906-16.382813 0-22.632813 6.25-6.253906 16.382813-6.253906 22.632813 0l158.398437 158.398437c6.253906 6.25 6.253906 16.382813 0 22.632813-3.132813 3.117187-7.230469 4.671875-11.328125 4.671875zm0 0"/></svg>
            </button>
        </li>
    {/each}
    <li class="add" on:click={() => {document.getElementById('new-player-input').focus()}}>
        <span>+</span>
        <form on:submit|preventDefault={addPlayer}>
            <input type="text"
                   placeholder="New player"
                   id="new-player-input"
                   pattern="[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð]+"
                   bind:value={name}>
            <button type="submit" hidden></button>
        </form>
    </li>
</ul>

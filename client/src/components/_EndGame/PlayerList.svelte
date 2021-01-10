<script lang="ts">
    import {PLAYERS_STORE} from "../../stores";

    let players;
    PLAYERS_STORE.subscribe(value => players = value);
</script>

<style lang="sass">
    @import "src/styles/theme"

    ul
        list-style: none
        padding: 0
        margin: 80px 0 0

    li
        height: 110px
        font-size: 1.5rem
        font-weight: 500
        display: flex
        flex-direction: column
        align-items: center
        justify-content: center
        border-top: 1px solid $grey

        &:first-of-type
            background: $black !important
            color: white !important
            //height: 80px

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


        div
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

    .points
        color: $grey
        font-weight: 400
        font-size: 1rem
</style>

<ul id="playerlist">
    {#each players as {name, uuid, points}, nr}
        <li id="{uuid}">
            <span>{nr + 1}</span>
            <div>
                {name}
            </div>
            <div class="points">
                {points > 0 ? points : ''}
            </div>
        </li>
    {/each}
</ul>
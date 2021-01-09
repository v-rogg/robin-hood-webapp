<script lang="ts">
    function startGame() {
        fetch('/api/start', {method: 'POST'})
    }
</script>

<style lang="sass">
    @import "src/styles/theme"

    .start-game
        cursor: pointer
        width: max-content
        margin: 80px 3rem 0 auto
        display: flex
        justify-content: right
        align-items: center
        position: relative

        span
            margin-right: 1rem
            font-size: 1.5rem
            font-weight: 300

        svg
            position: relative
            display: block

        &--outer-circle, &--inner-circle
            fill: $black

        &:hover

            span
                color: $green

            .start-game--outer-circle
                fill: $green
            .start-game--inner-circle
                fill: $red
</style>

<div class="start-game" on:click={startGame}>
    <span>
        Start Game
    </span>
    <svg x="0px" y="0px" viewBox="0 0 70 70" width="70px" height="70px">
        <path class="start-game--outer-circle" d="M35,0C15.67,0,0,15.67,0,35s15.67,35,35,35s35-15.67,35-35S54.33,0,35,0z M35,62
            C20.09,62,8,49.91,8,35S20.09,8,35,8s27,12.09,27,27S49.91,62,35,62z"/>
        <path class="start-game--inner-circle" d="M35,53c-9.93,0-18-8.08-18-18c0-9.93,8.07-18,18-18c9.92,0,18,8.07,18,18C53,44.92,44.92,53,35,53z
             M35,26c-4.96,0-9,4.04-9,9c0,4.96,4.04,9,9,9c4.96,0,9-4.04,9-9C44,30.04,39.96,26,35,26z"/>
    </svg>
</div>
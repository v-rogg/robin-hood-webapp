<style lang="sass">
    @import "src/styles/theme"

    .next-buttons
        display: grid
        grid-template-columns: repeat(2, 1fr)

        div
            height: 160px
            display: flex
            align-items: center
            justify-content: center
            border-bottom: 1px solid $grey
            font-size: 1.5rem
            font-weight: 500

            &:not(&:last-of-type)
                border-left: 1px solid $grey

            &:hover
                cursor: pointer
                background: $grey

    .grey
        background: $lightgrey
</style>

<div class="next-buttons">
    <div class="grey" on:click={() => {fetch('/api/reset', {method: 'POST'})}}>
        New Game
    </div>
    <div on:click={() => {fetch('/api/next-leg', {method: 'POST'})}}>
        Next Leg
    </div>
</div>
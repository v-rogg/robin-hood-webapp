<style lang="sass">
    @import "src/styles/theme"

    #legend
        text-align: left
        margin: 80px auto 0 3rem
        display: flex
        flex-direction: column
        justify-content: center
        align-items: flex-start

        >div
            display: flex
            align-items: center

        .bolt
            margin-bottom: 1rem

    .svg__bolt, .svg__remove
        width: 1.5rem
        height: 1.5rem
        margin-right: 0.5rem

    .svg__bolt
        fill: $orange
</style>

<div id="legend">
    <div class="bolt">
        <svg class="svg__bolt" viewBox="0 0 192 192" xmlns="http://www.w3.org/2000/svg"><path d="m155.109 74.028a4 4 0 0 0 -3.48-2.028h-52.4l8.785-67.123a4.023 4.023 0 0 0 -7.373-2.614l-63.724 111.642a4 4 0 0 0 3.407 6.095h51.617l-6.962 67.224a4.024 4.024 0 0 0 7.411 2.461l62.671-111.63a4 4 0 0 0 .048-4.027z"/></svg>
        Checkout table enabled
    </div>
    <div class="remove">
        <svg class="svg__remove" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg"><path d="m256 512c-141.164062 0-256-114.835938-256-256s114.835938-256 256-256 256 114.835938 256 256-114.835938 256-256 256zm0-480c-123.519531 0-224 100.480469-224 224s100.480469 224 224 224 224-100.480469 224-224-100.480469-224-224-224zm0 0"/><path d="m176.8125 351.1875c-4.097656 0-8.195312-1.554688-11.308594-4.691406-6.25-6.25-6.25-16.382813 0-22.632813l158.398438-158.402343c6.253906-6.25 16.386718-6.25 22.636718 0s6.25 16.382812 0 22.636718l-158.402343 158.398438c-3.15625 3.136718-7.25 4.691406-11.324219 4.691406zm0 0"/><path d="m335.1875 351.1875c-4.09375 0-8.191406-1.554688-11.304688-4.691406l-158.398437-158.378906c-6.253906-6.25-6.253906-16.382813 0-22.632813 6.25-6.253906 16.382813-6.253906 22.632813 0l158.398437 158.398437c6.253906 6.25 6.253906 16.382813 0 22.632813-3.132813 3.117187-7.230469 4.671875-11.328125 4.671875zm0 0"/></svg>
        Remove player
    </div>
</div>
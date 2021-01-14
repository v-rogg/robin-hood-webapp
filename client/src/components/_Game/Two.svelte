<script lang="ts">
    import {onMount} from "svelte";
    import Two from "two.js";
    import {io} from "socket.io-client";

    let two;
    const socket = io('ws://192.168.178.48:3000');

    onMount(() =>  {
        two = new Two({
            autostart: true,
            type: Two.Types.canvas,
            height: 300,
            width: 300,
        }).appendTo(document.getElementById('two'));

        const scale = two.width/451;

        // let t4 = two.makeCircle(two.height / 2, two.height / 2, ((340) * scale) / 2);
        // t4.fill = "#0000FF";
        //
        // let t3 = two.makeCircle(two.height / 2, two.height / 2, ((318) * scale) / 2);
        // t3.fill = "#FFFFFF";
        //
        // let t2 = two.makeCircle(two.height / 2, two.height / 2, ((218) * scale) / 2);
        // t2.fill = "#0000FF";
        //
        // let t1 = two.makeCircle(two.height / 2, two.height / 2, ((196) * scale) / 2);
        // t1.fill = "#FFFFFF";
        //
        // let dbull = two.makeCircle(two.height / 2, two.height / 2, (32 * scale) / 2);
        // dbull.fill = "#0000FF";
        //
        // let bull = two.makeCircle(two.height / 2, two.height / 2, (14 * scale) / 2);
        // bull.fill = "#FF0000";

        socket.on('sensorDarts', data => {
            const ldata = JSON.parse(data)
            let c = two.makeCircle((ldata[0] * scale ) + (two.width / 2) , - (ldata[1] * scale) + ( two.height / 2) , 4)
            c.fill = '#FFFFFF'
            c.linewidth = 1
            let d = two.makeCircle((ldata[0] * scale ) + (two.width / 2) , - (ldata[1] * scale) + ( two.height / 2) , 10)
            d.fill = '#FFFFFF'
            d.noStroke()
            d.opacity = .25
            setTimeout(() => {
                c.remove()
                d.remove()
            }, 300)
        })

    })
</script>

<style lang="sass">
    #two
        position: absolute
        width: 300px
        margin: 0 auto
        left: 0
        right: 0
</style>

<div id="two"></div>
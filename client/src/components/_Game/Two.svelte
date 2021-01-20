<script lang="ts">
    import {onMount} from "svelte";
    import Two from "two.js";
    import {io} from "socket.io-client";
    import {loop_guard} from "svelte/internal";

    let two;
    const socket = io('ws://192.168.178.48:3000');

    onMount(() =>  {
        two = new Two({
            autostart: true,
            // type: Two.Types.canvas,
            height: 300,
            width: 300,
        }).appendTo(document.getElementById('two'));

        const scale = two.width/451;

        // let t4 = two.makeCircle(two.height / 2, two.height / 2, ((340) * scale) / 2);
        // t4.fill = "#0000FF";
        // let t3 = two.makeCircle(two.height / 2, two.height / 2, ((318) * scale) / 2);
        // t3.fill = "#FFFFFF";
        // let t2 = two.makeCircle(two.height / 2, two.height / 2, ((218) * scale) / 2);
        // t2.fill = "#0000FF";
        // let t1 = two.makeCircle(two.height / 2, two.height / 2, ((196) * scale) / 2);
        // t1.fill = "#FFFFFF";
        // let dbull = two.makeCircle(two.height / 2, two.height / 2, (32 * scale) / 2);
        // dbull.fill = "#0000FF";
        // let bull = two.makeCircle(two.height / 2, two.height / 2, (14 * scale) / 2);
        // bull.fill = "#FF0000";

        let dart = Array.from(Array(3), () => new Array(2));

        socket.on('sensorDarts', data => {
            const ldata = JSON.parse(data)
            console.log(ldata)
            for (let i = 0; i < ldata.length; i++) {
                if (dart[i][0]) {
                    dart[i][0].remove()
                }
                if (dart[i][1]) {
                    dart[i][1].remove()
                }

                const x = ldata[i][0] * scale
                const y = -ldata[i][1] * scale

                let c = two.makeCircle(x + (two.width / 2), y + (two.height / 2), 4)
                c.linewidth = 1
                let d = two.makeCircle(x + (two.width / 2), y + (two.height / 2), 10)
                d.noStroke()
                d.opacity = .25
                // c.fill = '#FFFFFF'
                // d.fill = '#FFFFFF'

                switch(i) {
                    case 0:
                        c.fill = '#00FFFF';
                        d.fill = '#00FFFF';
                        break;
                    case 1:
                        c.fill = '#FF00FF';
                        d.fill = '#FF00FF';
                        break;
                    case 2:
                        c.fill = '#FFFF00';
                        d.fill = '#FFFF00';
                        break;
                }

                dart[i][0] = c
                dart[i][1] = d
                // setTimeout(() => {
                //     c.remove()
                //     d.remove()
                // }, 500)
            }
        })

        socket.on('players', () => {
            dart.forEach(d => {
                d.forEach(c => {
                    c.remove()
                    c = null
                })
            })
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
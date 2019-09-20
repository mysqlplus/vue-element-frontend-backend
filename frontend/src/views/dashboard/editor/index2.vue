<template>
  <div class="dashboard-editor-container">
    <div id="containerId"></div>
  </div>
</template>

<script>
  import {mapGetters} from 'vuex'
  import * as d3 from "d3";


  export default {
    name: 'DashboardEditor',
    data() {
      return {
        emptyGif: 'https://wpimg.wallstcn.com/0e03b7da-db9e-4819-ba10-9016ddfdaed3',
        showGame: false,
        gameH: 500,
        containerId:''
      }
    },
    computed: {
      ...mapGetters([
        'name',
        'avatar',
        'roles'
      ])
    },
    created() {
      this.init()
    },
    methods: {
      init() {
        var width = 800;
        var height = 800;
        var svg = d3.select("#containerId").append('svg').attr('id', "mapSvg").attr('width', width).attr('height', height);
        var projection = d3.geo.mercator().center([5, 32]).scale(140).translate([width / 2, height / 2])
        var path = d3.geo.path().projection(projection)
        var mapG = svg.append('g').attr('id', "mapG")
        mapG.selectAll("path").data(root.features).enter().append("path").attr("class", "map-path")
          .attr("stroke", "#212121")
          .attr("stroke-width", 1)
          .attr("fill", "#808080")
          .attr("style", "display:block")
          .attr("d", path)
        svg.append("g").attr("id", "pointG")
        this.pushData()
      },
      pushData() {
        var data = [
          {
            from: [161.71533203124997, -10.387304687499991],
            to: [117.1115, 40.7071]
          },
          {
            from: [117.5744140625001, 4.17060546875004],
            to: [115.2686, 30.6628]
          },
          {
            from: [90.31328125000007, 47.676171874999994],
            to: [112.6758, 30.9979]
          },
          {
            from: [129.71972656249997, 42.47500000000005],
            to: [121.01931115058903, 23.436683457875347]
          },
          {
            from: [-85.73383789062493, 68.630126953125],
            to: [91.1865, 30.1465]
          },
          {
            from: [-63.938574218750006, -12.529687499999994],
            to: [115.2686, 30.6628]
          },
          {
            from: [15.000683593750011, 46.6259765625],
            to: [99.613, 24.0546]
          },
          {
            from: [106.75341796875003, 20.73505859375004],
            to: [117.1115, 40.7071]
          },
        ]
        var index = 1
        setInterval(function () {
          var n = data.length * Math.random();
          n = parseInt(n);
          if (n > 7) {
            n = 7
          }

          var p = d3.select('#pointG').append('svg').attr('id', 'paper' + index);
          this.runAttack('paper' + index, data[n]);
          index++
        }, 200)
      }
    },
    runAttack() {
      var s = Snap('#' + id);
      var projection = d3.geo.mercator()
        .center([5, 32])
        .scale(140)
        .translate([width / 2, height / 2]);

      function makePro(arr) {
        var centroid = projection(arr),
          x = centroid[0],
          y = centroid[1];
        return [x, y]
      }

      var circleF = s.circle(makePro(data.from)[0], makePro(data.from)[1], 0);
      var circleT = s.circle(makePro(data.to)[0], makePro(data.to)[1], 0);
      var lineL = s.line(makePro(data.from)[0], makePro(data.from)[1], makePro(data.from)[0], makePro(data.from)[1]);
      circleF.attr({
        fill: "rgba(0,0,0,0)",
        stroke: "r()rgba(24,255,253,0.5)-#34A1FF",
        'stroke-width': "5px"
      });
      circleT.attr({
        fill: "#18FFFD",
        stroke: "r()#34A1FF-rgba(24,255,253,0.5)",
        'stroke-width': "8px"
      });
      lineL.attr({
        stroke: "L(" + makePro(data.to)[0] + "," + makePro(data.to)[1] + "," + makePro(data.from)[0] + "," + makePro(data.from)[1] + ")#18FFFD-rgba(0,225,132,0.1)",
        'stroke-width': "1px",
        fill: "rgba(0,0,0,0)"
      });

      circleF.animate({r: 20, 'stroke-width': "1px"}, 600, function () {
        circleF.remove();
      });
      lineL.animate({x2: makePro(data.to)[0], y2: makePro(data.to)[1]}, 500, mina.easeinout, function () {
        lineL.animate({
          x1: makePro(data.to)[0],
          y1: makePro(data.to)[1],
          'stroke-width': '0'
        }, 500, mina.easein, function () {
          lineL.remove();
        })

        circleT.animate({r: 10}, 1000, function () {
          circleT.remove();
          s.remove();
        })
      });
    },
  }
</script>

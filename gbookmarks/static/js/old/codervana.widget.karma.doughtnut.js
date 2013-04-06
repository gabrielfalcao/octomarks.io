$(function(){
    var options = {
	//Boolean - Whether we should show a stroke on each segment
	segmentShowStroke : true,

	//String - The colour of each segment stroke
	segmentStrokeColor : "#fff",

	//Number - The width of each segment stroke
	segmentStrokeWidth : 2,

	//The percentage of the chart that we cut out of the middle.
	percentageInnerCutout : 50,

	//Boolean - Whether we should animate the chart
	animation : true,

	//Number - Amount of animation steps
	animationSteps : 100,

	//String - Animation easing effect
	animationEasing : "easeOutBounce",

	//Boolean - Whether we animate the rotation of the Doughnut
	animateRotate : true,

	//Boolean - Whether we animate scaling the Doughnut from the centre
	animateScale : false,

	//Function - Will fire on animation completion.
	onAnimationComplete : null
    }
    var data = [
	{
	    value: 30,
	    color:"#FF1443",
            description: "Red Devil"
	},
	{
	    value : 50,
	    color : "#FF782D",
            description: "Mellow Orange"
	},
	{
	    value : 100,
	    color : "#FEFF9B",
            description: "Sunshine Shoulder"
	},
	{
	    value : 40,
	    color : "#66CC68",
            description: "Green Licorice"
	},
	{
	    value : 120,
	    color : "#5089C5",
            description: "Blue Hue"
	},
	{
	    value : 120,
	    color : "#8D50C5",
            description: "Purple Delite"
	},
	{
	    value : 142,
	    color : "#C550B1",
            description: "Deepest Pink"
	}
    ];
    var ctx = document.getElementById("myChart").getContext("2d");
    var karma_graph = new Chart(ctx).Doughnut(data, options);
});
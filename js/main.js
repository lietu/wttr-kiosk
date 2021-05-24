(function() {
    var img = document.getElementById("img")
    var src = img.src

    function cacheBuster(url) {
        return (url.split("?")[0]) + "?" + (Date.now())
    }

    function update() {
        img.src = cacheBuster(src)
    }

    function init() {
        setInterval(update, 1000)
    }

    init();
})()
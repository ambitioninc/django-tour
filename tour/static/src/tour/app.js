window.addEventListener('load', function() {
    var tourWraps = document.getElementsByClassName('tour-wrap');
    for (var i = 0; i < tourWraps.length; i++) {
        var itemCircles = tourWraps[i].getElementsByClassName('tour-item-circle');
        var numItems = itemCircles.length;
        if (numItems === 0) {
            break;
        }
        // Determine percentage offsets for circles
        var increment = 100.0 / numItems;
        for (var j = 0; j < numItems; j++) {
            itemCircles[j].style.right = (increment * (numItems - j - 1)) + '%';
        }
        // Find the current step
        var completedItems = tourWraps[i].getElementsByClassName('complete');
        if (completedItems.length) {
            var completedItem = completedItems[completedItems.length - 1];
            var completedDiv = tourWraps[i].getElementsByClassName('completed')[0];
            var right = parseFloat(completedItem.style.right);
            completedDiv.style.width = (100.0 - right) + '%';
        }

        // Unhide the bar
        var barWrap = tourWraps[i].getElementsByClassName('tour-bar-wrap')[0];
        barWrap.className = barWrap.className.replace('hidden', '');
    }
});

window.addEventListener('load', function() {
    var tourWraps = document.getElementsByClassName('tour-wrap');
    for (var i = 0; i < tourWraps.length; i++) {
        var stepCircles = tourWraps[i].getElementsByClassName('step-circle');
        var stepNames = tourWraps[i].getElementsByClassName('step-name');
        var numSteps = stepCircles.length;
        if (numSteps === 0) {
            break;
        }

        // Determine percentage offsets for circles
        var increment = 100.0 / numSteps;
        for (var j = 0; j < numSteps; j++) {
            stepCircles[j].style.right = (increment * (numSteps - j - 1)) + '%';
            stepNames[j].style.right = '0';
            if (j !== numSteps - 1) {
                var offset = -(stepNames[j].offsetWidth / 2) + (stepCircles[j].offsetWidth / 2)
                stepNames[j].style.marginRight = offset + 'px';
            }
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

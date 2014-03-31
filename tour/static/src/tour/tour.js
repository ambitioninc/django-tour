(function() {
    'use strict';

    /**
     * @constructor
     * There are currently no options to configure, so the constructor is empty
     */

    window.DjangoTour = function DjangoTour() {};

    window.DjangoTour.prototype = {

        /**
         * @method positionTourElements
         * Calculates and sets the x offset values for each circle element and step name element. Marks
         * a current step by setting a class and then shows the element.
         * @param {HTMLElement} tourWrap - The tour dom element containing all of the step data
         */
        positionTourElements: function positionTourElements(tourWrap) {
            // Query for the circle and name elements
            var stepCircles = tourWrap.getElementsByClassName('step-circle');
            var stepNames = tourWrap.getElementsByClassName('step-name');
            var numSteps = stepCircles.length;
            if (numSteps === 0) {
                return;
            }

            // Determine percentage offsets for circles
            var increment = 100.0 / numSteps;
            for (var i = 0; i < numSteps; i++) {
                stepCircles[i].style.right = (increment * (numSteps - i - 1)) + '%';
                stepNames[i].style.right = '0';
                if (i !== numSteps - 1) {
                    var offset = -(stepNames[i].offsetWidth / 2) + (stepCircles[i].offsetWidth / 2);
                    stepNames[i].style.marginRight = offset + 'px';
                }
            }

            // Find the current step
            var completedItems = tourWrap.getElementsByClassName('complete');
            if (completedItems.length) {
                var completedItem = completedItems[completedItems.length - 1];
                var completedDiv = tourWrap.getElementsByClassName('completed')[0];
                var right = parseFloat(completedItem.style.right);
                completedDiv.style.width = (100.0 - right) + '%';
            }

            // Unhide the bar
            var barWrap = tourWrap.getElementsByClassName('tour-bar-wrap')[0];
            barWrap.className = barWrap.className.replace('hidden', '');
        },

        /**
         * @method run
         * Gets all of the tour elements on the page and calls positionTourElements for each container
         */
        run: function run() {
            var tourWraps = document.getElementsByClassName('tour-wrap');
            for (var i = 0; i < tourWraps.length; i++) {
                this.positionTourElements(tourWraps[i]);
            }
        }
    };
})();

var tour = new window.DjangoTour();
tour.run();

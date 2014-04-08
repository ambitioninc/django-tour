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
            var circleWidth = 0;
            var numSteps = stepCircles.length;
            if (numSteps === 0) {
                return;
            }

            // Determine percentage offsets for circles
            var increment = 100.0 / numSteps;
            var currentStep = null;
            for (var i = 0; i < numSteps; i++) {
                stepCircles[i].style.right = (increment * (numSteps - i - 1)) + '%';
                circleWidth = stepCircles[i].offsetWidth;
                stepNames[i].style.right = '0';
                if (i !== numSteps - 1) {
                    var offset = -(stepNames[i].offsetWidth / 2) + (stepCircles[i].offsetWidth / 2);
                    stepNames[i].style.marginRight = offset + 'px';
                }

                // Check if this is the current step
                var classMap = {};
                var classNames = stepCircles[i].className.split(' ');
                for (var j = 0; j < classNames.length; j++) {
                    classMap[classNames[j]] = true;
                }

                if ('current' in classMap && 'available' in classMap) {
                    currentStep = stepCircles[i];
                } else if ('incomplete' in classMap && 'available' in classMap && i > 0 && !currentStep) {
                    currentStep = stepCircles[i];
                }
            }

            // Find the current step
            var completedDiv = tourWrap.getElementsByClassName('completed')[0],
                right = 0;

            // Set the width of the current progress bar
            if (currentStep) {
                right = parseFloat(currentStep.style.right);
                completedDiv.style.width = (100.0 - right) + '%';
                completedDiv.style.marginLeft = -(circleWidth / 2) + 'px';
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

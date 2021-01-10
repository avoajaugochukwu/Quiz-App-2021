
(function() {
    let slideUp = (target, duration=500) => {

        target.style.transitionProperty = 'height, margin, padding';
        target.style.transitionDuration = duration + 'ms';
        target.style.boxSizing = 'border-box';
        target.style.height = target.offsetHeight + 'px';
        target.offsetHeight;
        target.style.overflow = 'hidden';
        target.style.height = 0;
        target.style.paddingTop = 0;
        target.style.paddingBottom = 0;
        target.style.marginTop = 0;
        target.style.marginBottom = 0;
        window.setTimeout( () => {
              target.style.display = 'none';
              target.style.removeProperty('height');
            //   target.style.removeProperty('padding-top');
            //   target.style.removeProperty('padding-bottom');
            //   target.style.removeProperty('margin-top');
            //   target.style.removeProperty('margin-bottom');
            //   target.style.removeProperty('overflow');
            //   target.style.removeProperty('transition-duration');
            //   target.style.removeProperty('transition-property');
        }, duration);
    }


    document.querySelector('.unanswered_questions_btn')
        .addEventListener(
            'click', (e) => {
                e.preventDefault()
                let closeButton = document.querySelector('.unanswered_questions_alert')
                closeButton.style.display = "none"
                
                // slideUp(closeButton, 500)
            }
        )
})();
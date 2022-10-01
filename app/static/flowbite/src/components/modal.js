const Default = {
    placement: 'center',
    backdropClasses: 'bg-gray-900 bg-opacity-50 dark:bg-opacity-80 fixed inset-0 z-40',
    onHide: () => {
    },
    onShow: () => {
    },
    onToggle: () => {
    }
};

class Modal {
    constructor(targetEl = null, options = {}) {
        this._targetEl = targetEl;
        this._options = {...Default, ...options};
        this._isHidden = true;
        this._init();
    }

    _init() {
        this._getPlacementClasses().map((c) => {
            this._targetEl.classList.add(c);
        });
    }

    _createBackdrop() {
        if (this._isHidden) {
            const backdropEl = document.createElement('div');
            backdropEl.setAttribute('modal-backdrop', '');
            backdropEl.classList.add(...this._options.backdropClasses.split(' '));
            document.querySelector('body').append(backdropEl);
        }
    }

    _destroyBackdropEl() {
        if (!this._isHidden) {
            document.querySelector('[modal-backdrop]').remove();
        }
    }

    _getPlacementClasses() {
        switch (this._options.placement) {
            // top
            case 'top-left':
                return ['justify-start', 'items-start'];
            case 'top-center':
                return ['justify-center', 'items-start'];
            case 'top-right':
                return ['justify-end', 'items-start'];

            // center
            case 'center-left':
                return ['justify-start', 'items-center'];
            case 'center':
                return ['justify-center', 'items-center'];
            case 'center-right':
                return ['justify-end', 'items-center'];

            // bottom
            case 'bottom-left':
                return ['justify-start', 'items-end'];
            case 'bottom-center':
                return ['justify-center', 'items-end'];
            case 'bottom-right':
                return ['justify-end', 'items-end'];

            default:
                return ['justify-center', 'items-center'];
        }
    }

    toggle() {
        if (this._isHidden) {
            this.show();
        } else {
            this.hide();
        }

        // callback function
        this._options.onToggle(this);
    }

    show() {
        this._targetEl.classList.add('flex');
        this._targetEl.classList.remove('hidden');
        this._targetEl.setAttribute('aria-modal', 'true');
        this._targetEl.setAttribute('role', 'dialog');
        this._targetEl.removeAttribute('aria-hidden');
        this._createBackdrop();
        this._isHidden = false;

        // callback function
        this._options.onShow(this);
    }

    hide() {
        this._targetEl.classList.add('hidden');
        this._targetEl.classList.remove('flex');
        this._targetEl.setAttribute('aria-hidden', 'true');
        this._targetEl.removeAttribute('aria-modal');
        this._targetEl.removeAttribute('role');
        this._destroyBackdropEl();
        this._isHidden = true;

        // callback function
        this._options.onHide(this);
    }
}

window.Modal = Modal;

export default Modal;

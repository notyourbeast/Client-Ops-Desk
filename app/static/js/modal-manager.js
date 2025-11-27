/**
 * Centralized Modal Manager
 * Prevents modal collisions by managing z-index and ensuring only one modal is open at a time
 */

class ModalManager {
    constructor() {
        this.openModals = [];
        this.baseZIndex = 50;
        this.overlayZIndex = 40;
    }

    /**
     * Open a modal and ensure proper z-index stacking
     * @param {string} modalId - ID of the modal element
     * @param {Object} options - Options for modal behavior
     */
    open(modalId, options = {}) {
        const modal = document.getElementById(modalId);
        if (!modal) {
            console.error(`Modal with ID "${modalId}" not found`);
            return;
        }

        // Close any existing modals if preventMultiple is true (default)
        if (options.preventMultiple !== false) {
            this.closeAll();
        }

        // Calculate z-index based on number of open modals
        const zIndex = this.baseZIndex + this.openModals.length;
        const overlayZIndex = this.overlayZIndex + this.openModals.length;

        // Find or create overlay
        let overlay = modal.querySelector('.modal-overlay');
        if (!overlay && options.createOverlay !== false) {
            overlay = document.createElement('div');
            overlay.className = 'modal-overlay fixed inset-0 bg-black bg-opacity-50';
            overlay.style.zIndex = overlayZIndex;
            overlay.addEventListener('click', () => this.close(modalId));
            modal.insertBefore(overlay, modal.firstChild);
        }

        // Set modal z-index
        modal.style.zIndex = zIndex;
        modal.classList.remove('hidden');

        // Track this modal
        this.openModals.push({
            id: modalId,
            element: modal,
            overlay: overlay
        });

        // Prevent body scroll
        document.body.style.overflow = 'hidden';

        // Focus trap (optional)
        if (options.focusTrap !== false) {
            this.trapFocus(modal);
        }

        // Call onOpen callback if provided
        if (options.onOpen) {
            options.onOpen();
        }
    }

    /**
     * Close a specific modal
     * @param {string} modalId - ID of the modal element
     */
    close(modalId) {
        const modalIndex = this.openModals.findIndex(m => m.id === modalId);
        if (modalIndex === -1) return;

        const modalData = this.openModals[modalIndex];
        const modal = modalData.element;

        modal.classList.add('hidden');
        this.openModals.splice(modalIndex, 1);

        // Remove overlay if it was created by us
        if (modalData.overlay && modalData.overlay.parentNode === modal) {
            modalData.overlay.remove();
        }

        // Restore body scroll if no modals are open
        if (this.openModals.length === 0) {
            document.body.style.overflow = '';
        }

        // Call onClose callback if provided
        if (modal.dataset.onClose) {
            const callback = window[modal.dataset.onClose];
            if (typeof callback === 'function') {
                callback();
            }
        }
    }

    /**
     * Close all open modals
     */
    closeAll() {
        const modalIds = [...this.openModals.map(m => m.id)];
        modalIds.forEach(id => this.close(id));
    }

    /**
     * Trap focus within modal for accessibility
     * @param {HTMLElement} modal - Modal element
     */
    trapFocus(modal) {
        const focusableElements = modal.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        
        if (focusableElements.length === 0) return;

        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        const handleTab = (e) => {
            if (e.key !== 'Tab') return;

            if (e.shiftKey) {
                if (document.activeElement === firstElement) {
                    e.preventDefault();
                    lastElement.focus();
                }
            } else {
                if (document.activeElement === lastElement) {
                    e.preventDefault();
                    firstElement.focus();
                }
            }
        };

        modal.addEventListener('keydown', handleTab);
        firstElement.focus();
    }

    /**
     * Check if a modal is currently open
     * @param {string} modalId - ID of the modal element
     * @returns {boolean}
     */
    isOpen(modalId) {
        return this.openModals.some(m => m.id === modalId);
    }
}

// Create global instance
window.modalManager = new ModalManager();

// Close modals on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && window.modalManager.openModals.length > 0) {
        const lastModal = window.modalManager.openModals[window.modalManager.openModals.length - 1];
        window.modalManager.close(lastModal.id);
    }
});


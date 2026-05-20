/**
 * Gratia Frontend Core
 * Handles real-time updates and common UI interactions.
 */

const Gratia = {
    /**
     * Set loading state on a button
     * @param {HTMLElement} btn 
     * @param {boolean} isLoading 
     */
    setLoading: function(btn, isLoading) {
        if (!btn) return;
        if (isLoading) {
            btn.dataset.originalContent = btn.innerHTML;
            btn.disabled = true;
            btn.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processando...`;
        } else {
            btn.innerHTML = btn.dataset.originalContent || btn.innerHTML;
            btn.disabled = false;
        }
    },

    /**
     * Show a simple toast/alert feedback
     * @param {string} message 
     * @param {string} type - 'success' | 'error' | 'warning'
     */
    showFeedback: function(message, type = 'info') {
        // For now, using a simple alert. Can be expanded to a toast system.
        alert(message);
    }
};

// Initial setup for SocketIO if on a page that needs it
document.addEventListener('DOMContentLoaded', () => {
    // Shared initialization logic here
});

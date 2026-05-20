(function () {
    const DEFAULT_TIMEOUT = 12000;

    function setFeedback(region, tone, message) {
        if (!region) {
            return;
        }

        region.classList.remove('d-none', 'alert-info', 'alert-success', 'alert-warning', 'alert-danger');
        region.classList.add(`alert-${tone}`);
        region.textContent = message;
    }

    function resetFeedback(region) {
        if (!region) {
            return;
        }

        region.classList.add('d-none');
        region.textContent = '';
    }

    function setLoading(button, loadingText, isLoading) {
        if (!button) {
            return null;
        }

        if (isLoading) {
            if (!button.dataset.originalText) {
                button.dataset.originalText = button.innerHTML;
            }

            button.disabled = true;
            button.setAttribute('aria-busy', 'true');
            button.innerHTML = `
                <span class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>
                <span>${loadingText}</span>
            `;
            return null;
        }

        const originalText = button.dataset.originalText;
        if (originalText) {
            button.innerHTML = originalText;
        }
        button.disabled = false;
        button.removeAttribute('aria-busy');
        return null;
    }

    async function submitEnhancedForm(form) {
        const feedback = form.querySelector('[data-form-feedback]');
        const submitButton = form.querySelector('[type="submit"]');
        const loadingText = form.dataset.loadingText || 'Carregando...';
        const timeoutMs = Number.parseInt(form.dataset.timeoutMs || `${DEFAULT_TIMEOUT}`, 10);
        if (!form.checkValidity()) {
            form.classList.add('was-validated');
            setFeedback(feedback, 'warning', 'Corrija os campos destacados antes de continuar.');
            form.reportValidity();
            return;
        }

        const controller = new AbortController();
        const timeoutId = window.setTimeout(() => controller.abort(), timeoutMs);

        resetFeedback(feedback);
        setLoading(submitButton, loadingText, true);

        try {
            const response = await fetch(form.action, {
                method: form.method || 'POST',
                body: new FormData(form),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json, text/plain, */*'
                },
                signal: controller.signal,
                credentials: 'same-origin'
            });

            window.clearTimeout(timeoutId);

            if (response.redirected) {
                window.location.assign(response.url);
                return;
            }

            const contentType = response.headers.get('content-type') || '';
            let payloadMessage = '';
            let tone = response.ok ? 'success' : 'danger';

            if (contentType.includes('application/json')) {
                const payload = await response.json();
                payloadMessage = payload.message || payload.error || 'Operação concluída.';
                tone = response.ok ? 'success' : 'danger';
            } else {
                const text = await response.text();
                payloadMessage = text.trim() || (response.ok ? 'Operação concluída.' : 'Não foi possível concluir a operação.');
            }

            setFeedback(feedback, tone, payloadMessage);

            if (response.ok) {
                form.reset();
            }
        } catch (error) {
            window.clearTimeout(timeoutId);
            const message = error.name === 'AbortError'
                ? 'Tempo limite excedido. Tente novamente.'
                : 'Falha de comunicação. Verifique a conexão e tente novamente.';
            setFeedback(feedback, 'danger', message);
        } finally {
            setLoading(submitButton, loadingText, false);
        }
    }

    document.querySelectorAll('[data-enhanced-form]').forEach((form) => {
        form.addEventListener('submit', (event) => {
            event.preventDefault();
            submitEnhancedForm(form);
        });
    });
})();
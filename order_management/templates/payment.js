class PaymentManager {
    async createPayment(formData) {
        const response = await fetch('/payments', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        return response.json();
    }

    async loadPayments() {
        const response = await fetch('/payments');
        return response.json();
    }

    calculateGST(amount) {
        return (amount * 0.18).toFixed(2);
    }

    formatCurrency(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(amount);
    }
}

const paymentManager = new PaymentManager();

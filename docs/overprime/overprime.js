document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const correctStringInput = document.getElementById('correctString');
    const discountStringInput = document.getElementById('discountString');
    const ownerValInput = document.getElementById('ownerVal');
    const overprimeValInput = document.getElementById('overprimeVal');
    const differenceValDiv = document.getElementById('differenceVal');
    const btnCopy = document.getElementById('btnCopy');
    const btnReset = document.getElementById('btnReset');

    const spots = ["P5", "P4", "P3", "P2", "P1"];

    // Initial values
    correctStringInput.value = "Pawly 🐊 Arc 162 → 163 P5(48) P4(257) P3(1026) P2(3078) P1(6147)";

    // Event Listeners
    correctStringInput.addEventListener('input', parseAndCalculate);
    ownerValInput.addEventListener('input', parseAndCalculate);
    overprimeValInput.addEventListener('input', parseAndCalculate);

    btnCopy.addEventListener('click', () => {
        discountStringInput.select();
        discountStringInput.setSelectionRange(0, 99999); // For mobile devices
        navigator.clipboard.writeText(discountStringInput.value).then(() => {
            const originalText = btnCopy.textContent;
            btnCopy.textContent = 'Copied!';
            btnCopy.style.backgroundColor = '#4caf50';
            btnCopy.style.color = '#white';
            setTimeout(() => {
                btnCopy.textContent = originalText;
                btnCopy.style.backgroundColor = '';
                btnCopy.style.color = '';
            }, 1500);
        });
    });

    btnReset.addEventListener('click', reset);

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'r') {
            e.preventDefault();
            reset();
        }
    });

    // Run initial calculation
    parseAndCalculate();

    function parseAndCalculate() {
        const inputStr = correctStringInput.value;

        // Extract original values using regex
        const extractedVals = {};
        spots.forEach(spot => {
            const regex = new RegExp(`${spot}\\((\\d+)\\)`);
            const match = inputStr.match(regex);
            if (match) {
                extractedVals[spot] = parseInt(match[1], 10);
            } else {
                extractedVals[spot] = 0;
            }
        });

        // Update Original Values UI
        spots.forEach(spot => {
            document.getElementById(`orig-${spot}`).textContent = extractedVals[spot];
        });

        // Calculate Difference
        const ownerVal = parseInt(ownerValInput.value, 10) || 0;
        const overprimeVal = parseInt(overprimeValInput.value, 10) || 0;
        const difference = overprimeVal - ownerVal;
        differenceValDiv.textContent = difference;

        // Calculate distribution
        const totalSpots = Object.values(extractedVals).reduce((sum, val) => sum + val, 0);

        const profits = {};
        const discounts = {};
        spots.forEach(spot => {
            profits[spot] = 0;
            discounts[spot] = extractedVals[spot];
        });

        if (totalSpots > 0 && difference > 0) {
            // Distribute difference proportionally
            let allocatedProfit = 0;
            spots.forEach(spot => {
                const origVal = extractedVals[spot];
                const profit = Math.round(difference * (origVal / totalSpots));
                profits[spot] = profit;
                allocatedProfit += profit;
            });

            // Handle rounding discrepancies by adjusting the largest spot (P1)
            const discrepancy = difference - allocatedProfit;
            if (discrepancy !== 0) {
                profits["P1"] += discrepancy;
            }

            // Calculate discount values
            spots.forEach(spot => {
                discounts[spot] = Math.max(0, extractedVals[spot] - profits[spot]);
            });
        }

        // Update UI for Discount and Profit/Reduction
        spots.forEach(spot => {
            document.getElementById(`profit-${spot}`).textContent = profits[spot];
            document.getElementById(`disc-${spot}`).textContent = discounts[spot];
        });

        // Generate Output String
        let outputStr = inputStr;
        spots.forEach(spot => {
            const regex = new RegExp(`${spot}\\(\\d+\\)`, 'g');
            outputStr = outputStr.replace(regex, `${spot}(${discounts[spot]})`);
        });

        discountStringInput.value = outputStr;
    }

    function reset() {
        correctStringInput.value = "";
        discountStringInput.value = "";
        ownerValInput.value = "";
        overprimeValInput.value = "";
        differenceValDiv.textContent = "0";
        spots.forEach(spot => {
            document.getElementById(`orig-${spot}`).textContent = "0";
            document.getElementById(`disc-${spot}`).textContent = "0";
            document.getElementById(`profit-${spot}`).textContent = "0";
        });
    }
});

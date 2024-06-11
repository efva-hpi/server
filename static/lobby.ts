// HTML Elements
const leaveBtn = document.getElementById("leaveBtn");

// Event listeners

//leave lobby
leaveBtn?.addEventListener('click', () => {
    window.location.href = `${window.location.pathname}/leave`;
})
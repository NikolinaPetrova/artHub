document.addEventListener("DOMContentLoaded", () => {
    const bell = document.querySelector(".fa-bell");
    if (!bell) return;
    const dropdown = bell.closest(".dropdown").querySelector(".dropdown-menu");
    const countEl = document.getElementById("notification-count");
    let loaded = false;

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    async function loadCount() {
        try {
            const res = await fetch("/api/notifications/unread-count/");
            const data = await res.json();
            countEl.innerText = data.count > 0 ? data.count : "";
        } catch (err) {
            console.error("Error loading notification count:", err);
        }
    }

    async function loadNotifications() {
        try {
            const res = await fetch("/api/notifications/");
            const data = await res.json();
            dropdown.innerHTML = "";
            if (!data.length) {
                dropdown.innerHTML = "<p>Nothing new here.</p>";
                return;
            }

            data.forEach(n => {
                const li = document.createElement("li");

                const el = document.createElement("a");
                el.href = n.target_url;

                const wrapper = document.createElement("div");
                wrapper.classList.add("notification-item");

                const img = document.createElement("img");
                img.src = n.sender_avatar || "/static/images/user-default.jpg";
                img.classList.add("notif-avatar");

                const text = document.createElement("span");
                text.innerText = n.message;

                wrapper.appendChild(img);
                wrapper.appendChild(text);

                el.appendChild(wrapper);
                li.appendChild(el);
                dropdown.appendChild(li);

                el.addEventListener("click", async (e) => {
                    e.preventDefault();

                    try {
                        await fetch(`/api/notifications/${n.id}/read/`, {
                            method: "PATCH",
                            headers: {
                                "Content-Type": "application/json",
                                "X-CSRFToken": getCookie("csrftoken")
                            },
                            body: JSON.stringify({ is_read: true })
                        });

                        let currentCount = parseInt(countEl.innerText) || 0;
                        if (currentCount > 0) {
                            countEl.innerText = currentCount - 1 || "";
                        }

                        li.remove();

                        if (!dropdown.children.length) {
                            dropdown.innerHTML = "<p>Nothing new here.</p>";
                        }

                    } catch (err) {
                        console.error("Error marking notification as read:", err);
                    }

                    window.location.href = n.target_url;
                });
            });

        } catch (err) {
            console.error("Error loading notifications:", err);
        }
    }

    bell.addEventListener("click", async () => {
        const isVisible = dropdown.style.display === "block";
        dropdown.style.display = isVisible ? "none" : "block";

        if (!loaded && !isVisible) {
            await loadNotifications();
            loaded = true;
        }
    });

    document.addEventListener("click", (e) => {
        const isClickInsideDropdown = dropdown.contains(e.target);
        const isClickOnBell = bell.contains(e.target);

        if (!isClickInsideDropdown && !isClickOnBell) {
            dropdown.style.display = "none";
        }
    });

    loadCount();
});

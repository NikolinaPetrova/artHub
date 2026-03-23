document.addEventListener("DOMContentLoaded", function () {
    const toggles = document.querySelectorAll(".dropdown-toggle");
    toggles.forEach(toggle => {
        toggle.addEventListener("click", function () {
            const dropdown = this.parentElement;
            document.querySelectorAll(".dropdown").forEach(d => {
                if (d !== dropdown) {
                    d.classList.remove("active");
                }
            });
            dropdown.classList.toggle("active");
        });
    });

    document.addEventListener("click", function(e){
        if(!e.target.closest(".dropdown")){
            document.querySelectorAll(".dropdown").forEach(d=>{
                d.classList.remove("active");
            });
        }
    });

});
$(async function(){
    let savedJob = document.getElementsByClassName('saved')

    // Update DOM for saving a job
    $(".star").click(async function(e){
        const $tgt = $(e.target)
        const $closestLi = $tgt.closest("li")
        $tgt.closest("i").toggleClass("far fas")
        $closestLi.toggleClass("not-saved saved")
        console.log(savedJob)
        


        // if ($tgt.hasClass("fas")) {
        //     $closestLi.classList.add("saved")
        //     $closestLi.classList.remove("not-saved")
        // } else {
        //     $closestLi.classList.add("not-saved")
        //     $closestLi.classList.remove("saved")
        // }
    })
})
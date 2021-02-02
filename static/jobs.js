const BASE_URL = "http://127.0.0.1:5000/api";

$(async function(){
    let savedJob = document.getElementsByClassName('saved')
    let savedJobsIdArr = []



    // Update DOM for saving a job
    $(".star").click(async function(e){
        e.preventDefault()
        const $tgt = $(e.target)
        const $closestLi = $tgt.closest("li")
        let titleSpan = $closestLi.find('.job-header')
        let $jobTitle = titleSpan.get(0).id
        console.log($jobTitle)
        // console.log($jobTitle.get(0).id)
        $tgt.closest("i").toggleClass("far fas")
        $closestLi.toggleClass("not-saved saved")
        


        // Find Li parent element ID and save Look for status 200
        let $jobId = (e.target.closest("li").id)
        let userId = window.location.pathname.slice(8)

        async function saveJob($jobId, userId){
            const res = await axios.post(`${BASE_URL}/saved-jobs`, {saved_job_id: $jobId, user_id: userId, job_title: $jobTitle});

        }
        saveJob($jobId, userId, $jobTitle)

        // if (savedJobsIdArr.includes($jobId) == false){
        //     savedJobsIdArr.push($jobId);
        // }
        // else {
        //     let index = savedJobsIdArr.indexOf($jobId);
        //     if (index > -1){
        //         savedJobsIdArr.splice(index, 1)
        //     }
        // }

        })




    // async function getJobs(){
    //     const response = await axios.get('https://remotive.io/api/remote-jobs')
        
    //     for (let i=0; i<response.data.jobs.length; i++){
    //         allJobIdsArr.push(response.data.jobs[i].id);
    //         console.log(allJobIdsArr)

    //     }
    //     console.log(response.data.jobs.length)
    // }
    // getJobs()
    
// Pseudo: If any job from AJAX response has a matching ID to ones in savedJobsIdArr >
// retrieve the rest of the job data from the matching job and display it on the DOM.
// If the job is removed from favorites, update DOM
    })
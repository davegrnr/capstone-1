const BASE_URL = "http://127.0.0.1:5000/api";


$(async function(){
    $('.collapse').collapse()

    let userId = window.location.pathname.slice(8)

    async function getSavedJobs(){
        const res = await axios.get(`${BASE_URL}/saved-jobs/${userId}`);
        let jobData = res.data
        let jobIdArr = jobData.map(x => x.job_id)
        console.log(jobIdArr)
        }
        
    
    getSavedJobs();

    // Update DOM for saving a job
    $(".star").click(async function(e){
        e.preventDefault()
        // Pulling various data from the DOM 
        // (Need to revise to save all JSON and pull from that)
        const $tgt = $(e.target)
        const $closestLi = $tgt.closest("li")
        let titleSpan = $closestLi.find('.job-header')
        let $jobTitle = titleSpan.get(0).id
        let $jobId = (e.target.closest("li").id)
        let companyNameP = $closestLi.find('.company-name')
        let companyName = companyNameP.get(0).id

        // Toggle saved job star icon
        $tgt.closest("i").toggleClass("far fas")
        $closestLi.toggleClass("not-saved saved")
        
        

        async function saveJob($jobId, userId, $jobTitle){
            const res = await axios.post(`${BASE_URL}/saved-jobs`, {saved_job_id: $jobId, user_id: userId, job_title: $jobTitle, company_name: companyName});


        }
        saveJob($jobId, userId, $jobTitle, companyName)

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
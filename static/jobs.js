const BASE_URL = "http://127.0.0.1:5000/api";

let allJobIds = []
let jobIdArr = []


$(async function(){
    // get user id
    let userId = window.location.pathname.slice(8)

    $('.collapse').collapse()
    
    // populate array of all job ids from DOM
    async function getAllJobIds(){
        $("#search-results").find("li").each(function(){ allJobIds.push(this.id)})
        for(let i=0; i<allJobIds.length; i++){
            allJobIds[i] = +allJobIds[i];
        }
    }
    
    // populate array of saved job ids from API
    async function getSavedJobs(){
        const res = await axios.get(`${BASE_URL}/saved-jobs/${userId}`);
        let jobData = res.data
        let jobIdArr = jobData.map(x => x.job_id)

        // if job is saved, update DOM with star icon filled in
        for (let i=0; i<jobIdArr.length; i++){
            if (allJobIds.includes(jobIdArr[i]) == true){
                let j = $('#search-results').find(`#${jobIdArr[i]}`).children().find("#star")
                j.removeClass("far").addClass("fas")
                    continue;
            }
        }
        }
        
    getSavedJobs(); 

    // Update DOM for saving a job
    $(".star").click(async function(e){
        e.preventDefault()
        // Pulling various data from the DOM  for saving a job
        const $tgt = $(e.target)
        const $closestLi = $tgt.closest("li")
        let titleSpan = $closestLi.find('.job-header')
        let $jobTitle = titleSpan.get(0).id
        let $jobId = (e.target.closest("li").id)
        let companyNameP = $closestLi.find('.company-name')
        let companyName = companyNameP.get(0).id

        // Toggle saved job star icon
        $tgt.closest("i").toggleClass("far fas")
        if ($tgt.closest("i").hasClass('fas') === true){
            $('.toast').toast('show')}

        $closestLi.toggleClass("not-saved saved")
        
        // send saved job data to API
        async function saveJob($jobId, userId, $jobTitle){
            const res = await axios.post(`${BASE_URL}/saved-jobs`, {saved_job_id: $jobId, user_id: userId, job_title: $jobTitle, company_name: companyName});


        }

        saveJob($jobId, userId, $jobTitle, companyName)
        })
        getAllJobIds()

    })
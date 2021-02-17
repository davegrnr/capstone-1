const BASE_URL = "https://job-locker.herokuapp.com/api";

let allJobIds = []
let jobIdArr = []

function showSnackbar() {
    // Get the snackbar DIV
    var x = document.getElementById("snackbar");
  
    // Add the "show" class to DIV
    x.className = "show";
  
    // After 3 seconds, remove the show class from DIV
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 1500);
  }

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
        let jobUrl = $closestLi.find('#job-url').html()


        $tgt.closest("i").toggleClass("far fas")
        
        if ($tgt.closest("i").hasClass('fas') === true){
            // $('.toast').toast('show')}
            showSnackbar();
        }

        $closestLi.toggleClass("not-saved saved")
        
        // send saved job data to API
        async function saveJob($jobId, userId, $jobTitle, companyName, jobUrl){
            const res = await axios.post(`${BASE_URL}/saved-jobs`, {saved_job_id: $jobId, user_id: userId, job_title: $jobTitle, company_name: companyName, job_url: jobUrl});

        }


        

        saveJob($jobId, userId, $jobTitle, companyName, jobUrl)
        })
        getAllJobIds()

    })
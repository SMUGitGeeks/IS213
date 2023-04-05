const create_job_URL = "http://localhost:5007/create_job"

const app = Vue.createApp({

    //=========== DATA PROPERTIES ===========
    data() {
        return {
            job_role: "",
            job_company: "",
            job_description: "",
            new_skill: "",
            skills: [],
            job_added: false,
            add_job_error: "",
            api_key: ""
        }
    },

    //=========== METHODS ===========
    methods: {

        add_skill() {
            let skill = this.new_skill
            this.skills.push(skill)
            this.new_skill = ""
        },

        submitForm() {
            this.job_added = false;
            this.add_job_error = "";

            let jsonData = JSON.stringify({
                "job_role": this.job_role,
                "job_company": this.job_company,
                "job_description": this.job_description,
                "jobskills": this.skills,
                "api_key": this.api_key
            });

            fetch(`${create_job_URL}`,
                {
                    method: "POST",
                    headers: {
                        "Content-type": "application/json"
                    },
                    body: jsonData
                })
                .then(response => response.json())
                .then(data => {

                    if (data.code >= 200 && data.code < 300) {
                        this.job_added = true
                        this.job_role = ""
                        this.job_description = ""
                        this.job_company = ""
                        this.api_key = ""
                        this.skills = []

                    } else {
                        this.add_job_error = data.message;
                    }

                })
        },

        delete_skill(i) {
            this.skills.splice(i, 1)
        }

    }
})


app.mount('#app')
(function () {
    console.log('Hello!');
})();

function handleClick(type) {
    const user_text_name = document.getElementById("user_text_name").value;
    const user_text = document.getElementById("user_text").value;

    let modal_close = document.getElementById('modal-close')

    document.getElementById("user_text_name").value = ""
    document.getElementById("user_text").value = ""
    modal_close.click();


    fetch('/tasks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({name: user_text_name, text_data: user_text}),
    })
        .then(response => response.json())
        .then(data => {
            getStatus(data.task_id)
        })
}

function getStatus(taskID) {
    fetch(`/tasks/${taskID}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    })
        .then(response => response.json())
        .then(res => {
            console.log(res)
            const html = `<tr>
                            <td>${taskID}</td>
                            <td>${res.task_status}</td>
                            <td>${res.task_result}</td>
                          </tr>`;
            if (!document.getElementById(taskID)) {
                const newRow = document.getElementById('tasks').insertRow(0);
                newRow.setAttribute("id", taskID)
                newRow.innerHTML = html;
            }

            const taskStatus = res.task_status;
            if (taskStatus === 'SUCCESS' || taskStatus === 'FAILURE') {
                const task_row = document.getElementById(taskID)
                task_row.innerHTML = html;
                getReport(taskID)
                return false;
            }

            setTimeout(function () {
                getStatus(taskID);
            }, 1000);
        })
        .catch(err => console.log(err));
}

function getReport(taskID) {
    fetch(`/reports/${taskID}`, {
        method: 'get',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(),
    })
        .then(response => response.json())
        .then(res => {
            if (res) {
                const html = `<tr>
                            <td>${res.id}</td>
                            <td>${res.name}</td>
                            <td>
                                <form action="reports/${res.id}/html">
                                    <input type="submit" class="btn btn-html" value="Go to html"/>
                                </form>
                            </td>
                          </tr>`;
                const newRow = document.getElementById('reports').insertRow(0);
                newRow.innerHTML = html;
            }
        })
}
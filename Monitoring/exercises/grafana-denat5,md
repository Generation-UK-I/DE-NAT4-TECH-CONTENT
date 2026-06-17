# Grafana

This exercise will get you to start up an instance of Grafana. You will set up two data sources and display them in a dashboard on different panels.

## Grafana prep

We now need to run two containers, one for Grafana and one for a data source of coffee sales.

### Docker setup

This lab uses Docker containers which you can run on your CentOS VM.

To make them easier to find the files required for this lab have been packaged into a [grafana-demo](./grafana-demo.zip) zip file which you should download.

We need to move these files into your VM, so make a new working directory on your VM, then you can either:

1. Unzip the files on your local computer, open each one (there are only 5), then re-create them in your Linux VM - ensure you match the filenames.
1. Copy the whole zip to your VM and unzip them there directly. To do so open a terminal in the same directory as the downloaded zip, then copy it to the VM with `scp grafana-demo.zip centos@[VM_IP-ADDR]:/home/centos/[new_directory]`. You'll be prompted to enter your password, then see the file being copied.

Now you can deploy your containers. In your VM, in your new working directory, with the files unzipped:

1. Run `docker ps -a` to check for old containers
    - Stop any running ones with `docker stop <container_name>`
1. Run `sudo docker compose up -d`

You should see your new deployment being built.

### The container setup

This is what will now be running:

![](../img/grafana-flask.png)<!-- .element: class="centered" -->

### Check Grafana is running

1. Confirm that you can see the Grafana dashboard by opening <http://localhost:3000> on your browser
1. You can login with the default credentials - username `admin` and password `admin`. It will ask you to choose a new password, input whatever you want here

### Data source setup

The scripts above also start a containerised Flask app running on port `5000` which generates some dummy Coffee Shop data for us to display in Grafana. The source code for the Flask app lives in [../handouts/app.py](../handouts/app.py), and is set up via file [../handouts/Dockerfile.data](../handouts/Dockerfile.data).

Once you have logged into the Grafana dashboard, you can tell Grafana where to look for data. We will be using a combination of the data generated from `app.py`, as well as a test database that comes with Grafana.

You can see this by browsing to <http://localhost:5000/sales_stats>.

>**JUNE 2026** - The following instructions are a bit out of date in regards to the specific UI elements. It can be completed, but you might have to explore a little to find the correct options.

1. Make sure you are on the Grafana UI at <http://localhost:3000> and have logged in as above
1. Click to expand the left hand side menu, then select `Connections` - `Data Sources`
1. Select `Add data source`
1. Select `Infinity` from the list
    1. Filter the list for `Infinity` if you can't see it
1. Click the blue `Add new data source` button
1. The Name should have the default `yesoreyeram-infinity-datasource` displayed
    1. This is from <https://grafana.com/grafana/plugins/yesoreyeram-infinity-datasource/?tab=overview>
    1. It is pre-installed in our container via file [../handouts/Dockerfile.grafana](../handouts/Dockerfile.grafana)
1. Click the blue `Save & Test` button
1. Wait for the green `OK. Settings saved` message to be displayed

### Setting up a dashboard

Now that we have the relevant data source plugin installed, we can hook up a custom json data source to grafana in order to generate some visualisation panels for a dashboard we will put together.

#### Visualising data from a third-party API

1. Click to expand the left hand side menu, then click on `Dashboards`.
1. Click the blue `New` dropdown button on the top right and select `New dashboard`.
1. Select `+ Add visualization`,
    1. Then under `Select data source` select `yesoreyeram-infinity-datasource`.
1. Under `Table View` switch the toggle `on`
    1. Some default test data should be displayed.
1. Select the `Transform data` tab under the table view, and then `+ Add transformation`.
1. Scroll down and select the `Group by` transformation tile.
1. Next to `country` select `Group by` in the dropdown.
1. Next to `age` select `Calculate`, then `Count`.
1. A transformed view of the data should appear.
1. Under `Visualisations` on the top right select the `Bar Chart` view.
1. Under `Panel options`, set the `Title` field to be "User count by country".
1. Under `Bar Chart` on the right, find `X Axis` and change it to `country`.
1. Under `Table View` switch the toggle off.
1. Select the `Save Dashboard` blue button in the top right corner.
    1. Give it a title like "User data".
1. This will take us to our new dashboard with a generated graph.
    1. Click on "Dashboards" on te left navbar.
    1. Click on your dashboard name to display it in "view" mode.

#### Visualising data from a local custom API

Let's use the containerised data source running on port 5000 to visualise some coffee shop sales stats in grafana!

1. On the dashboard we just created, select the `Add` button on the top right and then the `Visualisation` option.
1. Under the panel view, change the URL field to `http://data_source:5000/sales_stats`.
1. Scroll down to `Parsing options & Result fields` and expand the section.
    1. Enter `stats` into the `Rows/Root` field.
1. Click the `Add columns` button;
    1. Put `recorded_date` in the `Selector` box and format as `Time`.
1. Click `Add columns` again;
    1. Put `coffee_sales` in the `Selector` box, `Coffee Sales` in the `Title` box, and format as `Number`.
1. Click `Add columns` one last time;
    1. Put `food_sales` in the `Selector` box, `Food Sales` in the `Title` box, and format as `Number`.
1. Click the refresh button in the top right corner, you will see a message that says "Data outside time range", click the `Zoom to data` button.
1. Under `panel Option`, set the `Title` to `Cafe Sales Stats`.
1. Click the blue `Save Dashboard` button to save and view the panel on your dashboard.
    1. Click on "Dashboards" on te left navbar.
    1. Click on your dashboard name to display it in "view" mode.

### Changing our data

1. Select the dropdown next to the refresh button in the top right corner. Set the option to "5s" or "10s" to set the auto refresh time.
1. In `app.py`, change the first `coffee_sales` value from `45.0` to `150.0`.
1. The `coffee_sales` line on the grafana panel should now update!
1. Stop the data source app using `docker stop data_source` or `podman stop data_source`, and see what happens to the panel. It will automagically tell us that there is no data to display.

### Changing our panels

There are plenty of ways of displaying data in Grafana. How do we change how our data is being displayed?

For the initial user data panel we set up:

1. Press the three dots to the right of `Panel Title` to bring up the menu and select `Edit`
1. Play with the options in the `Transform Data` tab and explore different visualization styles.

### Final Project

For your final project you will need to setup an EC2 instance which will use Docker to run Grafana for you. (I.e. one EC2 instance per team). This should be done using CloudFormation.

In your project time, refer to:

- For Generation: [./final-project-grafana-setup.md](./final-project-grafana-setup.md) file.
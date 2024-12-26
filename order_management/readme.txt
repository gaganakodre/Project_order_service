-- cmds used to create folders and files

mkdir -p order_management/{api,controllers,models,utils,templates,static}
touch order_management/api/app.py
touch order_management/controllers/order_controller.py
touch order_management/models/order.py
touch order_management/utils/{config.py,connection.py,rds_helper.py}
touch order_management/templates/index.html
touch order_management/static/{style.css,script.js}
touch order_management/schema.sql


--
python -m venv venv
source venv/Scripts/activate

-- run
python -m order_management.api.app

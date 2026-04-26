mkdir jtm; cd jtm

mkdir app
cd app

mkdir api, core, models, schemas, services, repositories, tests
mkdir api\routes

ni main.py

ni api\routes\auth.py
ni api\routes\clubs.py
ni api\routes\tournaments.py
ni api\routes\participants.py
ni api\routes\registrations.py

ni core\config.py
ni core\database.py
ni core\security.py

ni models\user.py
ni models\club.py
ni models\participant.py
ni models\tournament.py
ni models\registration.py

ni schemas\user.py
ni schemas\club.py
ni schemas\participant.py
ni schemas\tournament.py
ni schemas\registration.py

ni services\registration_service.py
ni services\validation_service.py
ni services\category_service.py

ni repositories\participant_repository.py
ni repositories\registration_repository.py
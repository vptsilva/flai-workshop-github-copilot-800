from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing data...')
        
        # Delete all existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Existing data cleared'))
        
        # Create teams
        self.stdout.write('Creating teams...')
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Earth\'s Mightiest Heroes'
        )
        team_dc = Team.objects.create(
            name='Team DC',
            description='Justice League Alliance'
        )
        
        self.stdout.write(self.style.SUCCESS(f'Created teams: {team_marvel.name}, {team_dc.name}'))
        
        # Create Marvel heroes
        self.stdout.write('Creating Marvel heroes...')
        marvel_heroes = [
            {'name': 'Tony Stark', 'email': 'ironman@marvel.com', 'hero_name': 'Iron Man'},
            {'name': 'Steve Rogers', 'email': 'captain@marvel.com', 'hero_name': 'Captain America'},
            {'name': 'Natasha Romanoff', 'email': 'blackwidow@marvel.com', 'hero_name': 'Black Widow'},
            {'name': 'Bruce Banner', 'email': 'hulk@marvel.com', 'hero_name': 'Hulk'},
            {'name': 'Thor Odinson', 'email': 'thor@marvel.com', 'hero_name': 'Thor'},
            {'name': 'Peter Parker', 'email': 'spiderman@marvel.com', 'hero_name': 'Spider-Man'},
        ]
        
        marvel_users = []
        for hero_data in marvel_heroes:
            user = User.objects.create(
                name=hero_data['name'],
                email=hero_data['email'],
                hero_name=hero_data['hero_name'],
                team_id=str(team_marvel._id)
            )
            marvel_users.append(user)
        
        # Create DC heroes
        self.stdout.write('Creating DC heroes...')
        dc_heroes = [
            {'name': 'Bruce Wayne', 'email': 'batman@dc.com', 'hero_name': 'Batman'},
            {'name': 'Clark Kent', 'email': 'superman@dc.com', 'hero_name': 'Superman'},
            {'name': 'Diana Prince', 'email': 'wonderwoman@dc.com', 'hero_name': 'Wonder Woman'},
            {'name': 'Barry Allen', 'email': 'flash@dc.com', 'hero_name': 'Flash'},
            {'name': 'Arthur Curry', 'email': 'aquaman@dc.com', 'hero_name': 'Aquaman'},
            {'name': 'Hal Jordan', 'email': 'greenlantern@dc.com', 'hero_name': 'Green Lantern'},
        ]
        
        dc_users = []
        for hero_data in dc_heroes:
            user = User.objects.create(
                name=hero_data['name'],
                email=hero_data['email'],
                hero_name=hero_data['hero_name'],
                team_id=str(team_dc._id)
            )
            dc_users.append(user)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(marvel_users) + len(dc_users)} users'))
        
        # Create activities for users
        self.stdout.write('Creating activities...')
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weightlifting', 'Yoga', 'Boxing', 'CrossFit']
        all_users = marvel_users + dc_users
        
        activities_created = 0
        for user in all_users:
            # Create 5-10 activities per user
            num_activities = random.randint(5, 10)
            for i in range(num_activities):
                activity_type = random.choice(activity_types)
                duration = random.randint(20, 120)  # 20-120 minutes
                distance = round(random.uniform(2, 20), 2) if activity_type in ['Running', 'Cycling', 'Swimming'] else None
                calories = duration * random.randint(5, 12)  # Calories burned
                days_ago = random.randint(0, 30)
                
                Activity.objects.create(
                    user_id=str(user._id),
                    activity_type=activity_type,
                    duration=duration,
                    distance=distance,
                    calories=calories,
                    date=timezone.now() - timedelta(days=days_ago)
                )
                activities_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {activities_created} activities'))
        
        # Create leaderboard entries
        self.stdout.write('Creating leaderboard entries...')
        rank = 1
        for user in all_users:
            user_activities = Activity.objects.filter(user_id=str(user._id))
            total_activities = user_activities.count()
            total_calories = sum([a.calories for a in user_activities])
            total_duration = sum([a.duration for a in user_activities])
            
            team = team_marvel if str(user.team_id) == str(team_marvel._id) else team_dc
            
            Leaderboard.objects.create(
                user_id=str(user._id),
                user_name=user.hero_name,
                team_id=str(team._id),
                team_name=team.name,
                total_activities=total_activities,
                total_calories=total_calories,
                total_duration=total_duration,
                rank=rank
            )
            rank += 1
        
        # Sort leaderboard by total_calories and update ranks
        leaderboard_entries = list(Leaderboard.objects.all().order_by('-total_calories'))
        for idx, entry in enumerate(leaderboard_entries, start=1):
            entry.rank = idx
            entry.save()
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(all_users)} leaderboard entries'))
        
        # Create workout suggestions
        self.stdout.write('Creating workout suggestions...')
        workouts = [
            {
                'name': 'Iron Man Circuit',
                'description': 'High-intensity circuit training for building strength and endurance like Tony Stark',
                'activity_type': 'CrossFit',
                'difficulty': 'advanced',
                'duration': 45,
                'calories_estimate': 450
            },
            {
                'name': 'Captain\'s Shield Training',
                'description': 'Military-style workout focusing on core strength and stamina',
                'activity_type': 'Weightlifting',
                'difficulty': 'intermediate',
                'duration': 60,
                'calories_estimate': 500
            },
            {
                'name': 'Black Widow Agility',
                'description': 'Combat-ready agility and flexibility training',
                'activity_type': 'Yoga',
                'difficulty': 'intermediate',
                'duration': 40,
                'calories_estimate': 280
            },
            {
                'name': 'Hulk Smash Workout',
                'description': 'Maximum strength training for explosive power',
                'activity_type': 'Weightlifting',
                'difficulty': 'advanced',
                'duration': 50,
                'calories_estimate': 550
            },
            {
                'name': 'Thor\'s Hammer Time',
                'description': 'God-like strength and conditioning workout',
                'activity_type': 'CrossFit',
                'difficulty': 'advanced',
                'duration': 60,
                'calories_estimate': 600
            },
            {
                'name': 'Web-Slinger Cardio',
                'description': 'Fast-paced cardio workout inspired by Spider-Man',
                'activity_type': 'Running',
                'difficulty': 'beginner',
                'duration': 30,
                'calories_estimate': 300
            },
            {
                'name': 'Batman\'s Night Patrol',
                'description': 'Stealth and endurance training for the Dark Knight',
                'activity_type': 'Running',
                'difficulty': 'intermediate',
                'duration': 45,
                'calories_estimate': 450
            },
            {
                'name': 'Superman Flight Training',
                'description': 'Full-body strength and power workout',
                'activity_type': 'Weightlifting',
                'difficulty': 'advanced',
                'duration': 55,
                'calories_estimate': 580
            },
            {
                'name': 'Wonder Woman Warrior',
                'description': 'Combat conditioning and warrior strength training',
                'activity_type': 'Boxing',
                'difficulty': 'intermediate',
                'duration': 50,
                'calories_estimate': 500
            },
            {
                'name': 'Flash Speed Training',
                'description': 'Speed and agility workout for maximum velocity',
                'activity_type': 'Running',
                'difficulty': 'intermediate',
                'duration': 35,
                'calories_estimate': 400
            },
            {
                'name': 'Aquaman Ocean Swim',
                'description': 'Intense swimming workout for full-body conditioning',
                'activity_type': 'Swimming',
                'difficulty': 'intermediate',
                'duration': 45,
                'calories_estimate': 450
            },
            {
                'name': 'Green Lantern Willpower',
                'description': 'Mental and physical endurance training',
                'activity_type': 'Yoga',
                'difficulty': 'beginner',
                'duration': 40,
                'calories_estimate': 250
            },
        ]
        
        for workout_data in workouts:
            Workout.objects.create(**workout_data)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(workouts)} workout suggestions'))
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(f'Teams: {Team.objects.count()}')
        self.stdout.write(f'Users: {User.objects.count()}')
        self.stdout.write(f'Activities: {Activity.objects.count()}')
        self.stdout.write(f'Leaderboard Entries: {Leaderboard.objects.count()}')
        self.stdout.write(f'Workouts: {Workout.objects.count()}')
        self.stdout.write(self.style.SUCCESS('================================='))

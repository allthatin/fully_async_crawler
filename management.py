import argparse
from workers import worker

async def execute_from_command_line(argv, session):
    parser = argparse.ArgumentParser(description='Manage your web crawler.')
    parser.add_argument('command', type=str, help='The command to run.')
    args = parser.parse_args(argv[1:])

    if args.command == 'run_worker':
        await worker(session)
    else:
        print(f'Unknown command: {args.command}')

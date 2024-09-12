import csv
import datetime
from typing import Annotated
import typer
import settings
from auth import auth

app = typer.Typer()


@app.command()
def login(
    force: Annotated[
        bool, typer.Option("--force", "-f", help="Force authentication")
    ] = False
) -> None:
    """
    Login user and record authorzation token and time for auditting usage
    """
    print("[green]Authenticating KIS API ...[/green]")
    try:
        if force:
            print("[red]Force reauthentication.[/red]")
            raise ValueError()
        with open(settings.AUTH_CSV_PATH) as f:
            revoked_at = datetime.datetime.strptime(
                f.readlines()[-1].split(",")[1].strip(), "%Y-%m-%d %H:%M:%S.%f"
            )
            if revoked_at > datetime.datetime.now():
                print("[green]You're already authenticated.[/green]")
                raise typer.Exit()
            else:
                print("[red]Auth token has been revoked.[/red]")
                print("[red]Requesting new auth token ... [/red]")
                raise ValueError()
    except (ValueError, FileNotFoundError):
        with open(settings.AUTH_CSV_PATH, "a+") as f:
            writer = csv.writer(f)
            auth_response = auth()
            authenticated_at = datetime.datetime.now()
            revoked_at = authenticated_at + datetime.timedelta(days=1)
            writer.writerow(
                [authenticated_at, revoked_at, auth_response["access_token"]]
            )
        print("[green]Successfully authenticated :rocket:![/green]")

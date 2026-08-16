from unittest.mock import Mock, patch
import cli


@patch("cli.requests.request")
def test_cli_list(mock_request, capsys):
    response = Mock()
    response.json.return_value = {
        "count": 1,
        "inventory": [{"id": 1, "name": "Test"}],
    }
    mock_request.return_value = response

    with patch("sys.argv", ["cli.py", "list"]):
        cli.main()

    output = capsys.readouterr().out
    assert "inventory" in output
    mock_request.assert_called_once_with(
        "GET", "http://127.0.0.1:5000/inventory", timeout=10
    )


@patch("cli.requests.request")
def test_cli_add(mock_request):
    response = Mock()
    response.json.return_value = {"id": 3, "name": "Apple", "price": 2.0, "stock": 5}
    mock_request.return_value = response

    with patch(
        "sys.argv",
        ["cli.py", "add", "--name", "Apple", "--price", "2", "--stock", "5"],
    ):
        cli.main()

    mock_request.assert_called_once()
    kwargs = mock_request.call_args.kwargs
    assert kwargs["json"]["name"] == "Apple"
    assert kwargs["json"]["price"] == 2.0
    assert kwargs["json"]["stock"] == 5

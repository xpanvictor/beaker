from beaker import *
from .nested_application import *


def demo():
    accts = sandbox.get_accounts()
    acct = accts.pop()

    # Create grandparent app and fund it
    app_client_grandparent = client.ApplicationClient(
        sandbox.get_algod_client(), Grandparent(), signer=acct.signer
    )
    grandparent_app_id, _, _ = app_client_grandparent.create()
    print(f"Created grandparent app: {grandparent_app_id}")
    app_client_grandparent.fund(1 * consts.algo)

    # Call the grandparent app to create the parent app
    result = app_client_grandparent.call(Grandparent.create_parent)
    parent_app_id = result.return_value
    print(f"Created parent app: {parent_app_id}")

    # Create parent app client
    app_client_parent = client.ApplicationClient(
        sandbox.get_algod_client(),
        Parent(),
        signer=acct.signer,
        app_id=parent_app_id,
    )

    app_client_parent.fund(1 * consts.algo)

    # Call the parent app to create the child_1 app
    result = app_client_parent.call(Parent.create_child_1)
    child_app_id = result.return_value
    print(f"Created child_1 app: {child_app_id}")

    # Create child_1 app client
    app_client_child = client.ApplicationClient(
        sandbox.get_algod_client(),
        Child1(),
        signer=acct.signer,
        app_id=child_app_id,
    )

    app_client_child.fund(1 * consts.algo)

    # Call the child_1 app to increment counter
    result = app_client_child.call(Child1.increment_counter)
    counter_value = result.return_value
    print(f"Counter value: {counter_value}")

    # Call the parent app to create the child_2 app
    result = app_client_parent.call(Parent.create_child_2)
    child_app_id = result.return_value
    print(f"Created child_2 app: {child_app_id}")

    # Create child_2 app client
    app_client_child = client.ApplicationClient(
        sandbox.get_algod_client(),
        Child2(),
        signer=acct.signer,
        app_id=child_app_id,
    )

    app_client_child.fund(1 * consts.algo)

    # Call the child_2 app to check lsig addr
    result = app_client_child.call(Child2.get_lsig_addr)
    addr_value = result.return_value
    print(f"LSig address value: {addr_value}")


if __name__ == "__main__":
    demo()

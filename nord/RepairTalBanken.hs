import qualified Data.Map as Map
type Id = Int -- actually this is a String like everything from XML
data FlatNode a = FlatNode a Id [Id] deriving (Eq, Show, Read)
data Tree a = Leaf a | Node a [Tree a] deriving (Eq, Show, Read)
type TalbankenInput = Map.Map Id (FlatNode String)

talbanken :: TalbankenInput
talbanken = Map.fromList [(10, FlatNode "foo" 10 [11, 100, 101])
                         , (11, FlatNode "bar" 11 [])
                         , (100, FlatNode "baz" 100 [])
                         , (101, FlatNode "qux" 101 [])]
build (FlatNode s id []) = Leaf s
build (FlatNode s id kids) = Node s (map (build . lookup) kids)
    where lookup = (talbanken Map.!)

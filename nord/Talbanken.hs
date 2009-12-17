module Talbanken where
type Id = Integer -- "s1_1" or "s1_501"
data FlatNode = FlatNode { cat :: String,
                           word :: String,
                           id :: Id,
                           kids::[Id] } deriving (Eq, Show, Read)
data Tree a = Leaf a a | Node a [Tree a] deriving (Eq, Read)
dat (Leaf a _) = a
dat (Node a _) = a
children (Leaf _ _) = []
children (Node _ kids) = kids
